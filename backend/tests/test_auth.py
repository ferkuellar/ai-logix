from app.db.session import SessionLocal
from app.models.audit_log import AuditLog


def test_auth_me_rejects_missing_token(anonymous_client):
    response = anonymous_client.get("/api/auth/me")

    assert response.status_code == 401


def test_auth_me_rejects_invalid_token(anonymous_client):
    response = anonymous_client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


def test_auth_me_returns_current_user(client, admin_user):
    response = client.get("/api/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == admin_user.email
    assert response.json()["role"] == "ADMIN"


def test_failed_login_creates_audit_log(anonymous_client, admin_user):
    response = anonymous_client.post(
        "/api/auth/login",
        json={"email": admin_user.email, "password": "wrong-password"},
    )

    assert response.status_code == 401

    db = SessionLocal()
    try:
        audit = db.query(AuditLog).filter(AuditLog.action == "LOGIN_FAILED").first()
        assert audit is not None
        assert audit.user_id == admin_user.id
        assert audit.metadata_json["email"] == admin_user.email
    finally:
        db.close()
