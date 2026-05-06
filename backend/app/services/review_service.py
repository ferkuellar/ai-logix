from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.delivery_event import DeliveryEvent
from app.models.order_state import OrderState


REVIEW_STATUS_PENDING = "OCR_PENDING"
REVIEW_STATUS_PROCESSED = "OCR_PROCESSED"
REVIEW_STATUS_REQUIRED = "HUMAN_REVIEW_REQUIRED"
REVIEW_STATUS_CONFIRMED = "HUMAN_CONFIRMED"
REVIEW_STATUS_REJECTED = "HUMAN_REJECTED"


def normalize_review_data(event: DeliveryEvent) -> dict:
    data = event.ai_extracted_json or {}
    review_status = data.get("review_status")

    if data.get("confirmed") is True:
        review_status = REVIEW_STATUS_CONFIRMED
    elif review_status in {REVIEW_STATUS_CONFIRMED, REVIEW_STATUS_REJECTED}:
        pass
    elif event.ocr_text or data:
        review_status = REVIEW_STATUS_REQUIRED
    else:
        review_status = REVIEW_STATUS_PENDING

    return {
        **data,
        "review_status": review_status,
        "confirmed": bool(data.get("confirmed", False)),
    }


def serialize_review_event(event: DeliveryEvent) -> dict:
    data = normalize_review_data(event)
    return {
        "event_id": event.id,
        "event_type": event.event_type,
        "order_number": event.order_number,
        "photo_url": event.photo_url,
        "ocr_text": event.ocr_text,
        "ai_extracted_json": data,
        "created_at": event.created_at,
        "review_status": data["review_status"],
        "status": event.status,
        "latitude": event.latitude,
        "longitude": event.longitude,
        "observations": event.observations,
        "confirmed_data": data.get("confirmed_data"),
    }


def get_review_event_or_404(db: Session, event_id: UUID) -> DeliveryEvent:
    event = db.query(DeliveryEvent).filter(DeliveryEvent.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery event was not found.",
        )
    return event


def ensure_event_has_ocr(event: DeliveryEvent) -> None:
    if not event.ocr_text and not event.ai_extracted_json:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Delivery event does not have processed OCR data.",
        )


def list_pending_reviews(
    db: Session,
    *,
    status_filter: str | None = None,
    order_number: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[dict]:
    query = db.query(DeliveryEvent).filter(
        (DeliveryEvent.ocr_text.isnot(None)) | (DeliveryEvent.ai_extracted_json.isnot(None))
    )

    if status_filter:
        query = query.filter(DeliveryEvent.status == status_filter)

    if order_number:
        query = query.filter(DeliveryEvent.order_number == order_number)

    events = (
        query.order_by(DeliveryEvent.created_at.desc())
        .offset(offset)
        .limit(min(max(limit, 1), 100))
        .all()
    )

    pending = []
    for event in events:
        data = normalize_review_data(event)
        if data["review_status"] in {REVIEW_STATUS_CONFIRMED, REVIEW_STATUS_REJECTED}:
            continue
        pending.append(serialize_review_event(event))

    return pending


def get_review_detail(db: Session, event_id: UUID) -> dict:
    event = get_review_event_or_404(db, event_id)
    ensure_event_has_ocr(event)
    return serialize_review_event(event)


def upsert_order_state(
    db: Session,
    *,
    event: DeliveryEvent,
    order_number: str,
    status_value: str,
) -> OrderState:
    order_state = (
        db.query(OrderState)
        .filter(OrderState.order_number == order_number)
        .first()
    )

    if not order_state:
        order_state = OrderState(order_number=order_number)
        db.add(order_state)

    order_state.current_status = status_value
    order_state.last_event_id = event.id
    order_state.last_latitude = event.latitude
    order_state.last_longitude = event.longitude
    order_state.last_update_at = datetime.utcnow()

    return order_state


def confirm_review(db: Session, event_id: UUID, confirmation: dict) -> DeliveryEvent:
    event = get_review_event_or_404(db, event_id)
    ensure_event_has_ocr(event)

    now = datetime.utcnow()
    current_data = normalize_review_data(event)
    confirmed_data = {
        "order_number": confirmation["order_number"],
        "store_code": confirmation.get("store_code"),
        "store_name": confirmation.get("store_name"),
        "barcode": confirmation.get("barcode"),
        "products": confirmation.get("products") or [],
        "status": confirmation["status"],
        "latitude": confirmation.get("latitude"),
        "longitude": confirmation.get("longitude"),
        "observations": confirmation.get("observations"),
    }

    event.order_number = confirmation["order_number"]
    event.status = confirmation["status"]
    event.latitude = confirmation.get("latitude")
    event.longitude = confirmation.get("longitude")
    event.observations = confirmation.get("observations")
    event.ai_extracted_json = {
        **current_data,
        "confirmed": True,
        "review_status": REVIEW_STATUS_CONFIRMED,
        "confirmed_at": now.isoformat(),
        "confirmed_data": confirmed_data,
    }

    upsert_order_state(
        db,
        event=event,
        order_number=confirmation["order_number"],
        status_value=confirmation["status"],
    )

    db.commit()
    db.refresh(event)
    return event


def reject_review(db: Session, event_id: UUID, rejection: dict) -> DeliveryEvent:
    event = get_review_event_or_404(db, event_id)
    ensure_event_has_ocr(event)

    current_data = normalize_review_data(event)
    event.ai_extracted_json = {
        **current_data,
        "confirmed": False,
        "review_status": REVIEW_STATUS_REJECTED,
        "rejection_reason": rejection["reason"],
        "rejection_observations": rejection.get("observations"),
        "rejected_at": datetime.utcnow().isoformat(),
    }
    if rejection.get("observations"):
        event.observations = rejection["observations"]

    db.commit()
    db.refresh(event)
    return event
