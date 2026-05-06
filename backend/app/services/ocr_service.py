from pathlib import Path
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.delivery_event import DeliveryEvent
from app.models.order_state import OrderState
from app.services.evidence_service import UPLOADS_ROOT
from app.services.file_validation import validate_local_image_file
from app.services.ocr_providers import MockOcrProvider, OpenAiOcrProvider, OcrProvider


REVIEW_STATUS_PENDING = "OCR_PENDING"
REVIEW_STATUS_PROCESSED = "OCR_PROCESSED"
REVIEW_STATUS_REQUIRED = "HUMAN_REVIEW_REQUIRED"
REVIEW_STATUS_CONFIRMED = "HUMAN_CONFIRMED"


def get_ocr_provider() -> OcrProvider:
    provider_name = settings.ocr_provider.lower()

    if provider_name == "mock":
        return MockOcrProvider()

    if provider_name == "openai":
        return OpenAiOcrProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Unsupported OCR_PROVIDER: {settings.ocr_provider}",
    )


def get_delivery_event_or_404(db: Session, event_id: UUID) -> DeliveryEvent:
    event = db.query(DeliveryEvent).filter(DeliveryEvent.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery event was not found.",
        )

    return event


def resolve_photo_path(photo_url: str | None) -> Path:
    if not photo_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delivery event does not have a photo_url.",
        )

    expected_prefix = "/uploads/"
    if not photo_url.startswith(expected_prefix):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only local uploaded evidence can be processed.",
        )

    relative_path = photo_url.removeprefix(expected_prefix)
    candidate = (UPLOADS_ROOT / relative_path).resolve()
    uploads_root = UPLOADS_ROOT.resolve()

    if uploads_root not in candidate.parents and candidate != uploads_root:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid evidence path.",
        )

    return candidate


def normalize_extracted_data(data: dict) -> dict:
    raw_text = str(data.get("raw_text") or "")

    return {
        "order_number": data.get("order_number"),
        "store_code": data.get("store_code"),
        "store_name": data.get("store_name"),
        "barcode": data.get("barcode"),
        "products": data.get("products") if isinstance(data.get("products"), list) else [],
        "status_suggestion": data.get("status_suggestion"),
        "observations": data.get("observations"),
        "confidence": float(data.get("confidence") or 0.0),
        "raw_text": raw_text,
        "confirmed": bool(data.get("confirmed", False)),
    }


def process_ocr_for_event(db: Session, event_id: UUID) -> DeliveryEvent:
    event = get_delivery_event_or_404(db, event_id)
    image_path = resolve_photo_path(event.photo_url)
    content_type = validate_local_image_file(image_path)
    provider = get_ocr_provider()

    try:
        extracted_data = normalize_extracted_data(
            provider.process_image(image_path, content_type=content_type)
        )
    except HTTPException:
        event.ai_extracted_json = {
            **(event.ai_extracted_json or {}),
            "ocr_status": "failed",
        }
        db.commit()
        raise

    event.ocr_text = extracted_data["raw_text"]
    event.ai_extracted_json = {
        **extracted_data,
        "ocr_status": "processed",
        "review_status": REVIEW_STATUS_REQUIRED,
        "provider": settings.ocr_provider.lower(),
    }

    db.commit()
    db.refresh(event)
    return event


def get_ocr_result(db: Session, event_id: UUID) -> DeliveryEvent:
    return get_delivery_event_or_404(db, event_id)


def upsert_order_state_from_ocr(
    db: Session,
    *,
    event: DeliveryEvent,
    order_number: str,
    status_value: str | None,
) -> OrderState:
    order_state = (
        db.query(OrderState)
        .filter(OrderState.order_number == order_number)
        .first()
    )

    if not order_state:
        order_state = OrderState(order_number=order_number)
        db.add(order_state)

    if status_value:
        order_state.current_status = status_value

    order_state.last_event_id = event.id
    if event.latitude is not None:
        order_state.last_latitude = event.latitude
    if event.longitude is not None:
        order_state.last_longitude = event.longitude

    return order_state


def confirm_ocr_result(db: Session, event_id: UUID, confirmation: dict) -> DeliveryEvent:
    event = get_delivery_event_or_404(db, event_id)
    current_data = event.ai_extracted_json or {}
    order_number = confirmation.get("order_number") or event.order_number or current_data.get("order_number")

    if not order_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="order_number is required to confirm OCR data.",
        )

    confirmed_data = {
        **current_data,
        "order_number": order_number,
        "store_code": confirmation.get("store_code"),
        "store_name": confirmation.get("store_name"),
        "barcode": confirmation.get("barcode"),
        "products": confirmation.get("products") or [],
        "status_suggestion": confirmation.get("status"),
        "observations": confirmation.get("observations"),
        "confirmed": True,
        "ocr_status": "confirmed",
        "review_status": REVIEW_STATUS_CONFIRMED,
    }

    event.order_number = order_number
    if confirmation.get("status"):
        event.status = confirmation["status"]
    if confirmation.get("observations"):
        event.observations = confirmation["observations"]
    event.ai_extracted_json = confirmed_data

    upsert_order_state_from_ocr(
        db,
        event=event,
        order_number=order_number,
        status_value=confirmation.get("status"),
    )

    db.commit()
    db.refresh(event)
    return event
