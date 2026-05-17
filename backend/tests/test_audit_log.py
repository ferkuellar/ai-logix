from app.db.session import SessionLocal
from app.models.audit_log import AuditLog


PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
)


def get_actions():
    db = SessionLocal()
    try:
        return {row.action for row in db.query(AuditLog).all()}
    finally:
        db.close()


def test_evidence_upload_and_ocr_create_audit_logs(client):
    uploaded = client.post(
        "/api/evidence/upload",
        data={"order_number": "AUDIT-OCR-1"},
        files={"file": ("audit.png", PNG_BYTES, "image/png")},
    )
    assert uploaded.status_code == 200

    processed = client.post(f"/api/ocr/process/{uploaded.json()['event_id']}")
    assert processed.status_code == 200

    actions = get_actions()
    assert "EVIDENCE_UPLOADED" in actions
    assert "OCR_PROCESSED" in actions


def test_human_review_confirm_and_reject_create_audit_logs(client):
    first = client.post(
        "/api/evidence/upload",
        data={"order_number": "AUDIT-REVIEW-CONFIRM"},
        files={"file": ("audit-confirm.png", PNG_BYTES, "image/png")},
    )
    assert first.status_code == 200
    first_event_id = first.json()["event_id"]
    assert client.post(f"/api/ocr/process/{first_event_id}").status_code == 200

    confirmed = client.post(
        f"/api/review/{first_event_id}/confirm",
        json={
            "order_number": "AUDIT-REVIEW-CONFIRMED",
            "status": "DELIVERED",
            "observations": "Audit test confirmation",
        },
    )
    assert confirmed.status_code == 200

    second = client.post(
        "/api/evidence/upload",
        data={"order_number": "AUDIT-REVIEW-REJECT"},
        files={"file": ("audit-reject.png", PNG_BYTES, "image/png")},
    )
    assert second.status_code == 200
    second_event_id = second.json()["event_id"]
    assert client.post(f"/api/ocr/process/{second_event_id}").status_code == 200

    rejected = client.post(
        f"/api/review/{second_event_id}/reject",
        json={"reason": "Audit test rejection"},
    )
    assert rejected.status_code == 200

    actions = get_actions()
    assert "HUMAN_REVIEW_CONFIRMED" in actions
    assert "HUMAN_REVIEW_REJECTED" in actions
