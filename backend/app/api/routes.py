from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status as http_status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db.session import get_db
from app.models.delivery_event import DeliveryEvent
from app.models.order_state import OrderState
from app.schemas.delivery_event import DeliveryEventCreate, DeliveryEventResponse
from app.schemas.evidence import EvidenceUploadResponse
from app.services.evidence_service import create_photo_uploaded_event, save_evidence_file

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-logix-backend"
    }


@router.post("/delivery-events", response_model=DeliveryEventResponse)
def create_delivery_event(
    payload: DeliveryEventCreate,
    db: Session = Depends(get_db)
):
    event = DeliveryEvent(**payload.model_dump())
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
        order_state.driver_id = payload.driver_id
        order_state.last_latitude = payload.latitude
        order_state.last_longitude = payload.longitude
        order_state.last_update_at = datetime.utcnow()

        db.commit()

    return event


@router.get("/order-states")
def list_order_states(db: Session = Depends(get_db)):
    return db.query(OrderState).all()


@router.post("/evidence/upload", response_model=EvidenceUploadResponse)
async def upload_evidence(
    order_number: str = Form(...),
    status: Optional[str] = Form(None),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    observations: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    order_number = order_number.strip()
    if not order_number:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="order_number is required.",
        )

    file_metadata = await save_evidence_file(file)
    event = create_photo_uploaded_event(
        db,
        order_number=order_number,
        status_value=status,
        latitude=latitude,
        longitude=longitude,
        observations=observations,
        file_metadata=file_metadata,
    )

    return {
        "event_id": event.id,
        "photo_url": event.photo_url,
        "metadata": event.payload_json,
    }
