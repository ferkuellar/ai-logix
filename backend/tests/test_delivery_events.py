from app.db.session import SessionLocal
from app.models.audit_log import AuditLog
from app.models.order_state import OrderState


def test_driver_can_create_delivery_event_and_order_state(driver_client):
    response = driver_client.post(
        "/api/delivery-events",
        json={
            "event_type": "STATUS_UPDATED",
            "order_number": "DRV-EVENT-1",
            "status": "DELIVERED",
            "latitude": 25.6866,
            "longitude": -100.3161,
        },
    )

    assert response.status_code == 200
    event = response.json()
    assert event["event_type"] == "STATUS_UPDATED"
    assert event["order_number"] == "DRV-EVENT-1"

    db = SessionLocal()
    try:
        state = db.query(OrderState).filter(OrderState.order_number == "DRV-EVENT-1").one()
        assert state.current_status == "DELIVERED"
        assert state.last_event_id is not None

        audit = db.query(AuditLog).filter(AuditLog.action == "DELIVERY_EVENT_CREATED").first()
        assert audit is not None
        assert audit.resource_id == event["id"]
    finally:
        db.close()


def test_delivery_event_without_order_number_does_not_create_order_state(driver_client):
    response = driver_client.post(
        "/api/delivery-events",
        json={"event_type": "STATUS_UPDATED", "status": "PENDING"},
    )

    assert response.status_code == 200

    db = SessionLocal()
    try:
        assert db.query(OrderState).count() == 0
    finally:
        db.close()
