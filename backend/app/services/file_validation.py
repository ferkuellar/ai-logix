from pathlib import Path

from fastapi import HTTPException, status


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024


def detect_image_type(header: bytes) -> str | None:
    if header.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"

    if header.startswith(b"\x89PNG"):
        return "image/png"

    if len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "image/webp"

    return None


def validate_image_content_type(content_type: str | None) -> str:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type. Use JPEG, PNG, or WEBP images.",
        )

    return content_type


def validate_image_magic_bytes(header: bytes, expected_content_type: str | None = None) -> str:
    detected_content_type = detect_image_type(header)

    if not detected_content_type:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid image file signature.",
        )

    if expected_content_type and detected_content_type != expected_content_type:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File signature does not match declared content type.",
        )

    return detected_content_type


def validate_local_image_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence image file was not found.",
        )

    with path.open("rb") as image_file:
        return validate_image_magic_bytes(image_file.read(16))
