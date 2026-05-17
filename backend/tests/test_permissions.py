PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
)


def upload_evidence(client, order_number="PERM-OCR-1"):
    response = client.post(
        "/api/evidence/upload",
        data={"order_number": order_number},
        files={"file": ("permission.png", PNG_BYTES, "image/png")},
    )
    assert response.status_code == 200
    return response.json()["event_id"]


def test_driver_cannot_list_order_states(driver_client):
    response = driver_client.get("/api/order-states")

    assert response.status_code == 403


def test_supervisor_can_list_order_states(supervisor_client):
    response = supervisor_client.get("/api/order-states")

    assert response.status_code == 200


def test_driver_cannot_process_ocr(driver_client, client):
    event_id = upload_evidence(client)

    response = driver_client.post(f"/api/ocr/process/{event_id}")

    assert response.status_code == 403


def test_supervisor_can_process_ocr(supervisor_client, client):
    event_id = upload_evidence(client, order_number="PERM-OCR-2")

    response = supervisor_client.post(f"/api/ocr/process/{event_id}")

    assert response.status_code == 200
    assert response.json()["ocr_text"]
