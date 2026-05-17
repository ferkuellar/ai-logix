PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
)


def test_upload_accepts_valid_image(client):
    response = client.post(
        "/api/evidence/upload",
        data={
            "order_number": "OX-UPLOAD-1",
            "status": "DELIVERED",
            "latitude": "25.6866",
            "longitude": "-100.3161",
        },
        files={"file": ("evidence.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["event_id"]
    assert body["photo_url"].startswith("/uploads/evidence/evidence_")
    assert body["metadata"]["content_type"] == "image/png"

    states = client.get("/api/order-states").json()
    uploaded_state = next(item for item in states if item["order_number"] == "OX-UPLOAD-1")
    assert uploaded_state["current_status"] == "DELIVERED"


def test_upload_rejects_invalid_content_type(client):
    response = client.post(
        "/api/evidence/upload",
        data={"order_number": "OX-BAD-TYPE"},
        files={"file": ("evidence.txt", b"not an image", "text/plain")},
    )

    assert response.status_code == 415


def test_upload_rejects_invalid_magic_bytes(client):
    response = client.post(
        "/api/evidence/upload",
        data={"order_number": "OX-BAD-MAGIC"},
        files={"file": ("evidence.png", b"not really a png", "image/png")},
    )

    assert response.status_code == 415


def test_upload_rejects_missing_order_number(client):
    response = client.post(
        "/api/evidence/upload",
        data={"order_number": " "},
        files={"file": ("evidence.png", PNG_BYTES, "image/png")},
    )

    assert response.status_code == 400
