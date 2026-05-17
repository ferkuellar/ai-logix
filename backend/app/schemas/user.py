from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


VALID_ROLES = {"ADMIN", "SUPERVISOR", "DRIVER"}


class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str = Field(min_length=8)
    role: str
    driver_id: Optional[UUID] = None

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if "@" not in value or value.startswith("@") or value.endswith("@"):
            raise ValueError("email must be a valid email-like identifier.")
        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        value = value.strip().upper()
        if value not in VALID_ROLES:
            raise ValueError("role must be ADMIN, SUPERVISOR or DRIVER.")
        return value


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    driver_id: Optional[UUID] = None
    is_active: Optional[bool] = None

    @field_validator("role")
    @classmethod
    def validate_optional_role(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip().upper()
        if value not in VALID_ROLES:
            raise ValueError("role must be ADMIN, SUPERVISOR or DRIVER.")
        return value


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str] = None
    role: str
    driver_id: Optional[UUID] = None
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
