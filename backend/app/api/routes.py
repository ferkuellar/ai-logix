from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status as http_status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.api.dependencies import require_driver_or_above, require_supervisor_or_admin, resolve_operational_driver_id
from app.db.session import get_db
from app.models.delivery_event import DeliveryEvent
from app.models.driver import Driver
from app.models.order_state import OrderState
from app.models.user import User
from app.schemas.delivery_event import DeliveryEventCreate, DeliveryEventResponse
from app.schemas.evidence import EvidenceUploadResponse
from app.schemas.ocr import (
    OcrConfirmRequest,
    OcrConfirmResponse,
    OcrProcessResponse,
    OcrResultResponse,
)
from app.services.evidence_service import create_photo_uploaded_event, save_evidence_file
from app.services.ocr_service import confirm_ocr_result, get_ocr_result, process_ocr_for_event
from app.services.audit_service import log_action

router = APIRouter()


def ensure_driver_exists(db: Session, driver_id: UUID | None) -> None:
    if driver_id is None:
        return
    if not db.query(Driver).filter(Driver.id == driver_id).first():
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="driver_id does not reference an existing driver.",
        )


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-logix-backend"
    }


@router.post("/delivery-events", response_model=DeliveryEventResponse)
def create_delivery_event(
    payload: DeliveryEventCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver_or_above),
):
    data = payload.model_dump()
    data["driver_id"] = resolve_operational_driver_id(current_user, data.get("driver_id"))
    ensure_driver_exists(db, data["driver_id"])

    event = DeliveryEvent(**data)
    db.add(event)
    db.commit()
    db.refresh(event)

    if payload.order_number:
        order_state = (
            db.query(OrderState)
            .filter(OrderState.order_number == payload.order_number)
            .first()
        )

        if not order_state:
            order_state = OrderState(order_number=payload.order_number)
            db.add(order_state)

        if payload.status:
            order_state.current_status = payload.status

        order_state.last_event_id = event.id
        order_state.store_id = payload.store_id
        order_state.driver_id = data["driver_id"]
        order_state.last_latitude = payload.latitude
        order_state.last_longitude = payload.longitude
        order_state.last_update_at = datetime.utcnow()

        db.commit()

    log_action(
        db,
        action="DELIVERY_EVENT_CREATED",
        resource_type="delivery_event",
        resource_id=str(event.id),
        user=current_user,
        metadata={"event_type": event.event_type, "order_number": event.order_number},
        ip_address=request.client.host if request.client else None,
    )

    return event


@router.get("/order-states")
def list_order_states(
    db: Session = Depends(get_db),
    _: User = Depends(require_supervisor_or_admin),
):
    return db.query(OrderState).all()


@router.post("/evidence/upload", response_model=EvidenceUploadResponse)
async def upload_evidence(
    request: Request,
    order_number: str = Form(...),
    status: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    observations: Optional[str] = Form(None),
    driver_id: Optional[UUID] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_driver_or_above),
):
    order_number = order_number.strip()
    if not order_number:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="order_number is required.",
        )

    resolved_driver_id = resolve_operational_driver_id(current_user, driver_id)
    ensure_driver_exists(db, resolved_driver_id)

    file_metadata = await save_evidence_file(file)
    event = create_photo_uploaded_event(
        db,
        order_number=order_number,
        driver_id=resolved_driver_id,
        status_value=status,
        latitude=latitude,
        longitude=longitude,
        observations=observations,
        file_metadata=file_metadata,
    )
    log_action(
        db,
        action="EVIDENCE_UPLOADED",
        resource_type="delivery_event",
        resource_id=str(event.id),
        user=current_user,
        metadata={"order_number": event.order_number, "photo_url": event.photo_url, "driver_id": str(event.driver_id) if event.driver_id else None},
        ip_address=request.client.host if request.client else None,
    )

    return {
        "event_id": event.id,
        "photo_url": event.photo_url,
        "metadata": event.payload_json,
    }


@router.post("/ocr/process/{event_id}", response_model=OcrProcessResponse)
def process_ocr(
    event_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisor_or_admin),
):
    event = process_ocr_for_event(db, event_id)
    log_action(
        db,
        action="OCR_PROCESSED",
        resource_type="delivery_event",
        resource_id=str(event.id),
        user=current_user,
        metadata={"order_number": event.order_number},
        ip_address=request.client.host if request.client else None,
    )

    return {
        "event_id": event.id,
        "ocr_text": event.ocr_text or "",
        "ai_extracted_json": event.ai_extracted_json,
    }


@router.get("/ocr/result/{event_id}", response_model=OcrResultResponse)
def read_ocr_result(
    event_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_supervisor_or_admin),
):
    event = get_ocr_result(db, event_id)

    return {
        "event_id": event.id,
        "event_type": event.event_type,
        "order_number": event.order_number,
        "photo_url": event.photo_url,
        "ocr_text": event.ocr_text,
        "ai_extracted_json": event.ai_extracted_json,
    }


@router.post("/ocr/confirm/{event_id}", response_model=OcrConfirmResponse)
def confirm_ocr(
    event_id: UUID,
    payload: OcrConfirmRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_supervisor_or_admin),
):
    event = confirm_ocr_result(db, event_id, payload.model_dump())

    return {
        "event_id": event.id,
        "confirmed": True,
        "ai_extracted_json": event.ai_extracted_json,
    }
