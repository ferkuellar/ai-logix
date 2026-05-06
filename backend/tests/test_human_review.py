PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
)


def upload_and_process(client, order_number="OX-REVIEW-1"):
    uploaded = client.post(
        "/api/evidence/upload",
        data={"order_number": order_number},
        files={"file": ("review.png", PNG_BYTES, "image/png")},
    )
    assert uploaded.status_code == 200
    event_id = uploaded.json()["event_id"]

    processed = client.post(f"/api/ocr/process/{event_id}")
    assert processed.status_code == 200
    return event_id


def valid_confirmation(order_number="PED-HUMAN-1"):
    return {
        "order_number": order_number,
        "store_code": "OX-CHIH-001",
        "store_name": "OXXO Centro",
        "barcode": "7501234567890",
        "products": [{"name": "Producto demo", "quantity": 2}],
        "status": "DELIVERED",
        "latitude": 28.6353,
        "longitude": -106.0889,
        "observations": "Confirmado manualmente despues de OCR",
    }


def test_review_pending_returns_unconfirmed_ocr_events(client):
    event_id = upload_and_process(client)

    response = client.get("/api/review/pending")

    assert response.status_code == 200
    body = response.json()
    assert any(item["event_id"] == event_id for item in body)
    pending = next(item for item in body if item["event_id"] == event_id)
    assert pending["review_status"] == "HUMAN_REVIEW_REQUIRED"


def test_review_detail_returns_event(client):
    event_id = upload_and_process(client)

    response = client.get(f"/api/review/{event_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["event_id"] == event_id
    assert body["ocr_text"]
    assert body["ai_extracted_json"]["order_number"] == "PED-0001"


def test_confirm_review_updates_ai_extracted_json(client):
    event_id = upload_and_process(client)

    response = client.post(
        f"/api/review/{event_id}/confirm",
        json=valid_confirmation(order_number="PED-AI-JSON"),
    )

    assert response.status_code == 200
    body = response.json()
    data = body["ai_extracted_json"]
    assert body["review_status"] == "HUMAN_CONFIRMED"
    assert data["confirmed"] is True
    assert data["confirmed_data"]["order_number"] == "PED-AI-JSON"
    assert data["confirmed_data"]["status"] == "DELIVERED"


def test_confirm_review_updates_order_state(client):
    event_id = upload_and_process(client)

    response = client.post(
        f"/api/review/{event_id}/confirm",
        json=valid_confirmation(order_number="PED-STATE-1"),
    )
    assert response.status_code == 200

    states = client.get("/api/order-states").json()
    confirmed_state = next(item for item in states if item["order_number"] == "PED-STATE-1")
    assert confirmed_state["current_status"] == "DELIVERED"
    assert confirmed_state["last_latitude"] == 28.6353
    assert confirmed_state["last_longitude"] == -106.0889


def test_reject_review_marks_human_rejected(client):
    event_id = upload_and_process(client)

    response = client.post(
        f"/api/review/{event_id}/reject",
        json={
            "reason": "La imagen esta borrosa y el OCR no es confiable",
            "observations": "Solicitar nueva foto al repartidor",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["review_status"] == "HUMAN_REJECTED"
    assert body["confirmed"] is False
    assert body["ai_extracted_json"]["rejection_reason"] == "La imagen esta borrosa y el OCR no es confiable"


def test_confirm_review_rejects_invalid_status(client):
    event_id = upload_and_process(client)
    payload = valid_confirmation()
    payload["status"] = "REVIEW_REJECTED"

    response = client.post(f"/api/review/{event_id}/confirm", json=payload)

    assert response.status_code == 422


def test_confirm_review_requires_order_number(client):
    event_id = upload_and_process(client)
    payload = valid_confirmation()
    payload["order_number"] = " "

    response = client.post(f"/api/review/{event_id}/confirm", json=payload)

    assert response.status_code == 422


def test_reject_review_requires_reason(client):
    event_id = upload_and_process(client)

    response = client.post(
        f"/api/review/{event_id}/reject",
        json={"reason": " ", "observations": "Sin razon valida"},
    )

    assert response.status_code == 422
