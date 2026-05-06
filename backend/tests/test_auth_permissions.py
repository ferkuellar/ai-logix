from app.db.session import SessionLocal
from app.models.audit_log import AuditLog
from app.models.user import User
from app.services.auth_service import verify_password

PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
)


def test_login_success(anonymous_client, admin_user):
    response = anonymous_client.post(
        "/api/auth/login",
        json={"email": admin_user.email, "password": "Password123!"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"


def test_login_invalid_password(anonymous_client, admin_user):
    response = anonymous_client.post(
        "/api/auth/login",
        json={"email": admin_user.email, "password": "bad-password"},
    )

    assert response.status_code == 401


def test_protected_endpoint_requires_token(anonymous_client):
    response = anonymous_client.get("/api/order-states")

    assert response.status_code == 401


def test_admin_can_list_users(client):
    response = client.get("/api/users")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_driver_cannot_access_review_pending(driver_client):
    response = driver_client.get("/api/review/pending")

    assert response.status_code == 403


def test_driver_can_upload_evidence(driver_client):
    response = driver_client.post(
        "/api/evidence/upload",
        data={"order_number": "DRIVER-ORDER-1"},
        files={"file": ("driver.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 200
    assert response.json()["event_id"]


def test_supervisor_can_access_review_pending(supervisor_client):
    response = supervisor_client.get("/api/review/pending")

    assert response.status_code == 200


def test_password_is_hashed(admin_user):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == admin_user.id).first()
        assert user.hashed_password != "Password123!"
        assert verify_password("Password123!", user.hashed_password)
    finally:
        db.close()


def test_audit_log_created_on_login(anonymous_client, admin_user):
    response = anonymous_client.post(
        "/api/auth/login",
        json={"email": admin_user.email, "password": "Password123!"},
    )
    assert response.status_code == 200

    db = SessionLocal()
    try:
        audit = db.query(AuditLog).filter(AuditLog.action == "LOGIN_SUCCESS").first()
        assert audit is not None
        assert audit.user_id == admin_user.id
    finally:
        db.close()
