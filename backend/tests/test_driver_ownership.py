from uuid import UUID, uuid4

from app.db.session import SessionLocal
from app.models.delivery_event import DeliveryEvent
from app.models.driver import Driver
from app.models.order_state import OrderState
from app.models.user import User
from app.services.auth_service import create_access_token


PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
)


def create_driver(name="Driver", phone="5551000000"):
    db = SessionLocal()
    try:
        driver = Driver(name=name, phone=phone, status="ACTIVE")
        db.add(driver)
        db.commit()
        db.refresh(driver)
        return driver
    finally:
        db.close()


def authenticated_client_for_user(anonymous_client, user):
    anonymous_client.headers.update({"Authorization": f"Bearer {create_access_token(user.id)}"})
    return anonymous_client


def test_admin_can_create_driver_user_with_valid_driver_id(client):
    driver = create_driver()

    response = client.post(
        "/api/users",
        json={
            "email": "new-driver@example.com",
            "full_name": "New Driver User",
            "password": "Password123!",
            "role": "DRIVER",
            "driver_id": str(driver.id),
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["role"] == "DRIVER"
    assert body["driver_id"] == str(driver.id)


def test_admin_cannot_create_driver_user_without_driver_id(client):
    response = client.post(
        "/api/users",
        json={
            "email": "missing-driver@example.com",
            "full_name": "Missing Driver",
            "password": "Password123!",
            "role": "DRIVER",
        },
    )

    assert response.status_code == 400


def test_admin_cannot_create_driver_user_with_unknown_driver_id(client):
    response = client.post(
        "/api/users",
        json={
            "email": "unknown-driver@example.com",
            "full_name": "Unknown Driver",
            "password": "Password123!",
            "role": "DRIVER",
            "driver_id": str(uuid4()),
        },
    )

    assert response.status_code == 400


def test_auth_me_returns_driver_id_for_driver(driver_client, driver_user):
    response = driver_client.get("/api/auth/me")

    assert response.status_code == 200
    assert response.json()["driver_id"] == str(driver_user.driver_id)


def test_driver_can_create_delivery_event_for_own_driver(driver_client, driver_user):
    response = driver_client.post(
        "/api/delivery-events",
        json={
            "event_type": "STATUS_UPDATED",
            "order_number": "OWN-DELIVERY-1",
            "driver_id": str(driver_user.driver_id),
            "status": "DELIVERED",
        },
    )

    assert response.status_code == 200
    assert response.json()["driver_id"] == str(driver_user.driver_id)


def test_driver_omitted_driver_id_is_assigned_to_self(driver_client, driver_user):
    response = driver_client.post(
        "/api/delivery-events",
        json={
            "event_type": "STATUS_UPDATED",
            "order_number": "OWN-DELIVERY-2",
            "status": "DELIVERED",
        },
    )

    assert response.status_code == 200
    assert response.json()["driver_id"] == str(driver_user.driver_id)


def test_driver_cannot_create_delivery_event_for_other_driver(driver_client):
    other_driver = create_driver(name="Other Driver", phone="5551000001")

    response = driver_client.post(
        "/api/delivery-events",
        json={
            "event_type": "STATUS_UPDATED",
            "order_number": "OTHER-DELIVERY-1",
            "driver_id": str(other_driver.id),
        },
    )

    assert response.status_code == 403


def test_unassigned_driver_cannot_create_delivery_event(anonymous_client, unassigned_driver_user):
    client = authenticated_client_for_user(anonymous_client, unassigned_driver_user)

    response = client.post(
        "/api/delivery-events",
        json={"event_type": "STATUS_UPDATED", "order_number": "UNASSIGNED-1"},
    )

    assert response.status_code == 403


def test_supervisor_can_create_delivery_event_for_any_valid_driver(supervisor_client):
    driver = create_driver(name="Supervisor Target", phone="5551000002")

    response = supervisor_client.post(
        "/api/delivery-events",
        json={
            "event_type": "STATUS_UPDATED",
            "order_number": "SUP-DELIVERY-1",
            "driver_id": str(driver.id),
        },
    )

    assert response.status_code == 200
    assert response.json()["driver_id"] == str(driver.id)


def test_admin_can_create_delivery_event_for_any_valid_driver(client):
    driver = create_driver(name="Admin Target", phone="5551000003")

    response = client.post(
        "/api/delivery-events",
        json={
            "event_type": "STATUS_UPDATED",
            "order_number": "ADM-DELIVERY-1",
            "driver_id": str(driver.id),
        },
    )

    assert response.status_code == 200
    assert response.json()["driver_id"] == str(driver.id)


def test_driver_can_upload_own_evidence(driver_client, driver_user):
    response = driver_client.post(
        "/api/evidence/upload",
        data={"order_number": "OWN-EVIDENCE-1"},
        files={"file": ("own.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 200
    event_id = response.json()["event_id"]

    db = SessionLocal()
    try:
        event = db.query(DeliveryEvent).filter(DeliveryEvent.id == UUID(event_id)).one()
        state = db.query(OrderState).filter(OrderState.order_number == "OWN-EVIDENCE-1").one()
        assert event.driver_id == driver_user.driver_id
        assert state.driver_id == driver_user.driver_id
    finally:
        db.close()


def test_driver_cannot_upload_evidence_for_other_driver(driver_client):
    other_driver = create_driver(name="Other Evidence Driver", phone="5551000004")

    response = driver_client.post(
        "/api/evidence/upload",
        data={"order_number": "OTHER-EVIDENCE-1", "driver_id": str(other_driver.id)},
        files={"file": ("other.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 403


def test_unassigned_driver_cannot_upload_evidence(anonymous_client, unassigned_driver_user):
    client = authenticated_client_for_user(anonymous_client, unassigned_driver_user)

    response = client.post(
        "/api/evidence/upload",
        data={"order_number": "UNASSIGNED-EVIDENCE-1"},
        files={"file": ("unassigned.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 403


def test_supervisor_can_upload_evidence_for_valid_driver(supervisor_client):
    driver = create_driver(name="Supervisor Evidence", phone="5551000005")

    response = supervisor_client.post(
        "/api/evidence/upload",
        data={"order_number": "SUP-EVIDENCE-1", "driver_id": str(driver.id)},
        files={"file": ("supervisor.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 200

    db = SessionLocal()
    try:
        event = db.query(DeliveryEvent).filter(DeliveryEvent.id == UUID(response.json()["event_id"])).one()
        assert event.driver_id == driver.id
    finally:
        db.close()


def test_metadata_contains_user_driver_id():
    assert "driver_id" in User.__table__.columns
