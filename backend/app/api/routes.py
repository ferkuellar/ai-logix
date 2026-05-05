from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.delivery_event import DeliveryEvent
from app.models.order_state import OrderState
from app.schemas.delivery_event import DeliveryEventCreate, DeliveryEventResponse

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

        db.commit()

    return event


@router.get("/order-states")
def list_order_states(db: Session = Depends(get_db)):
    return db.query(OrderState).all()