PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
)


def upload_evidence(client, order_number="OX-OCR-1"):
    response = client.post(
        "/api/evidence/upload",
        data={"order_number": order_number},
        files={"file": ("evidence.png", PNG_BYTES, "image/png")},
    )
    assert response.status_code == 200
    return response.json()["event_id"]


def test_ocr_process_mock_provider(client):
    event_id = upload_evidence(client)

    response = client.post(f"/api/ocr/process/{event_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["ocr_text"]
    assert body["ai_extracted_json"]["order_number"] == "PED-0001"
    assert body["ai_extracted_json"]["status_suggestion"] == "DELIVERED"


def test_ocr_process_missing_event(client):
    response = client.post("/api/ocr/process/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404


def test_ocr_process_event_without_photo(client):
    created = client.post(
        "/api/delivery-events",
        json={"event_type": "STATUS_UPDATED", "order_number": "OX-NO-PHOTO"},
    )
    assert created.status_code == 200

    response = client.post(f"/api/ocr/process/{created.json()['id']}")

    assert response.status_code == 400


def test_order_state_updates_after_ocr_confirm(client):
    event_id = upload_evidence(client, order_number="OX-OLD")
    processed = client.post(f"/api/ocr/process/{event_id}")
    assert processed.status_code == 200

    response = client.post(
        f"/api/ocr/confirm/{event_id}",
        json={
            "order_number": "PED-CONFIRMED-1",
            "store_code": "OX-CHIH-001",
            "store_name": "OXXO Centro",
            "barcode": "7501234567890",
            "products": [{"name": "Producto demo", "quantity": 2}],
            "status": "DELIVERED",
            "observations": "Confirmado manualmente desde OCR",
        },
    )

    assert response.status_code == 200
    assert response.json()["confirmed"] is True

    states = client.get("/api/order-states").json()
    confirmed_state = next(item for item in states if item["order_number"] == "PED-CONFIRMED-1")
    assert confirmed_state["current_status"] == "DELIVERED"
