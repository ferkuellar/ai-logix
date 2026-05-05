from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class OcrProduct(BaseModel):
    name: str
    quantity: int | float | None = None


class OcrExtractedData(BaseModel):
    order_number: Optional[str] = None
    store_code: Optional[str] = None
    store_name: Optional[str] = None
    barcode: Optional[str] = None
    products: list[dict[str, Any]] = Field(default_factory=list)
    status_suggestion: Optional[str] = None
    observations: Optional[str] = None
    confidence: float = 0.0
    raw_text: str = ""
    confirmed: bool = False


class OcrProcessResponse(BaseModel):
    event_id: UUID
    ocr_text: str
    ai_extracted_json: OcrExtractedData


class OcrResultResponse(BaseModel):
    event_id: UUID
    event_type: str
    order_number: Optional[str] = None
    photo_url: Optional[str] = None
    ocr_text: Optional[str] = None
    ai_extracted_json: Optional[dict[str, Any]] = None


class OcrConfirmRequest(BaseModel):
    order_number: Optional[str] = None
    store_code: Optional[str] = None
    store_name: Optional[str] = None
    barcode: Optional[str] = None
    products: list[dict[str, Any]] = Field(default_factory=list)
    status: Optional[str] = None
    observations: Optional[str] = None


class OcrConfirmResponse(BaseModel):
    event_id: UUID
    confirmed: bool
    ai_extracted_json: dict[str, Any]
