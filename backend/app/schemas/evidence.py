from pydantic import BaseModel
from uuid import UUID


class EvidenceMetadata(BaseModel):
    original_filename: str | None
    stored_filename: str
    content_type: str
    size_bytes: int


class EvidenceUploadResponse(BaseModel):
    event_id: UUID
    photo_url: str
    metadata: EvidenceMetadata
