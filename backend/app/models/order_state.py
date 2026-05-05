from sqlalchemy import Column, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.base import Base


class OrderState(Base):
    __tablename__ = "order_states"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_number = Column(String, unique=True, nullable=False)
    current_status = Column(String, default="PENDING")

    store_id = Column(UUID(as_uuid=True), nullable=True)
    driver_id = Column(UUID(as_uuid=True), nullable=True)
    last_event_id = Column(UUID(as_uuid=True), nullable=True)

    last_latitude = Column(Float, nullable=True)
    last_longitude = Column(Float, nullable=True)

    last_update_at = Column(DateTime, default=datetime.utcnow)