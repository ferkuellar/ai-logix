from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


VALID_DELIVERY_STATUSES = {"PENDING", "DELIVERED", "PARTIAL", "FAILED", "CANCELLED"}


class ReviewEventBase(BaseModel):
    event_id: UUID
    order_number: Optional[str] = None
    photo_url: Optional[str] = None
    ocr_text: Optional[str] = None
    ai_extracted_json: Optional[dict[str, Any]] = None
    created_at: Optional[datetime] = None
    review_status: str


class ReviewPendingResponse(ReviewEventBase):
    pass


class ReviewDetailResponse(ReviewEventBase):
    event_type: str
    status: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    observations: Optional[str] = None
    confirmed_data: Optional[dict[str, Any]] = None


class HumanConfirmRequest(BaseModel):
    order_number: str
    store_code: Optional[str] = None
    store_name: Optional[str] = None
    barcode: Optional[str] = None
    products: list[dict[str, Any]] = Field(default_factory=list)
    status: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    observations: Optional[str] = None

    @field_validator("order_number")
    @classmethod
    def order_number_is_required(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("order_number is required.")
        return value

    @field_validator("status")
    @classmethod
    def status_is_valid(cls, value: str) -> str:
        value = value.strip().upper()
        if value not in VALID_DELIVERY_STATUSES:
            allowed = ", ".join(sorted(VALID_DELIVERY_STATUSES))
            raise ValueError(f"status must be one of: {allowed}")
        return value


class HumanRejectRequest(BaseModel):
    reason: str
    observations: Optional[str] = None

    @field_validator("reason")
    @classmethod
    def reason_is_required(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("reason is required.")
        return value


class HumanReviewResponse(BaseModel):
    event_id: UUID
    review_status: str
    confirmed: bool = False
    ai_extracted_json: dict[str, Any]
