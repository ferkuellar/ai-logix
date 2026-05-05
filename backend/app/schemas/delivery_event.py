from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID


class DeliveryEventCreate(BaseModel):
    event_type: str
    order_number: Optional[str] = None
    driver_id: Optional[UUID] = None
    store_id: Optional[UUID] = None
    status: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    photo_url: Optional[str] = None
    ocr_text: Optional[str] = None
    ai_extracted_json: Optional[Dict[str, Any]] = None
    observations: Optional[str] = None
    payload_json: Optional[Dict[str, Any]] = None


class DeliveryEventResponse(DeliveryEventCreate):
    id: UUID

    class Config:
        from_attributes = True