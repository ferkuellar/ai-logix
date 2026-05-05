from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.delivery_event import DeliveryEvent
from app.models.order_state import OrderState


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
UPLOADS_ROOT = Path(__file__).resolve().parents[2] / "uploads"
EVIDENCE_DIR = UPLOADS_ROOT / "evidence"


def ensure_evidence_dir() -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


async def save_evidence_file(file: UploadFile) -> dict:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Use JPEG, PNG, or WEBP images.",
        )

    ensure_evidence_dir()
    extension = ALLOWED_IMAGE_TYPES[file.content_type]
    stored_filename = f"evidence_{uuid4()}{extension}"
    destination = EVIDENCE_DIR / stored_filename

    size_bytes = 0
    try:
        with destination.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                size_bytes += len(chunk)
                if size_bytes > MAX_FILE_SIZE_BYTES:
                    output.close()
                    destination.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="File exceeds the 10 MB size limit.",
                    )

                output.write(chunk)
    except HTTPException:
        raise
    except OSError as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not store evidence file.",
        ) from exc
    finally:
        await file.close()

    return {
        "original_filename": file.filename,
        "stored_filename": stored_filename,
        "content_type": file.content_type,
        "size_bytes": size_bytes,
        "photo_url": f"/uploads/evidence/{stored_filename}",
    }


def create_photo_uploaded_event(
    db: Session,
    *,
    order_number: str,
    file_metadata: dict,
    status_value: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    observations: Optional[str] = None,
) -> DeliveryEvent:
    event = DeliveryEvent(
        event_type="PHOTO_UPLOADED",
        order_number=order_number,
        status=status_value,
        latitude=latitude,
        longitude=longitude,
        observations=observations,
        photo_url=file_metadata["photo_url"],
        payload_json={
            "original_filename": file_metadata["original_filename"],
            "stored_filename": file_metadata["stored_filename"],
            "content_type": file_metadata["content_type"],
            "size_bytes": file_metadata["size_bytes"],
        },
    )
    db.add(event)
    db.commit()
    db.refresh(event)

    order_state = (
        db.query(OrderState)
        .filter(OrderState.order_number == order_number)
        .first()
    )

    if not order_state:
        order_state = OrderState(order_number=order_number)
        db.add(order_state)

    if status_value:
        order_state.current_status = status_value

    order_state.last_event_id = event.id
    if latitude is not None:
        order_state.last_latitude = latitude
    if longitude is not None:
        order_state.last_longitude = longitude
    order_state.last_update_at = datetime.utcnow()

    db.commit()

    return event
