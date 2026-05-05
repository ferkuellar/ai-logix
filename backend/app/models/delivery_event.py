from sqlalchemy import Column, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.db.base import Base


class DeliveryEvent(Base):
    __tablename__ = "delivery_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    event_type = Column(String, nullable=False)
    order_number = Column(String, nullable=True)

    driver_id = Column(UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=True)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"), nullable=True)

    status = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    photo_url = Column(String, nullable=True)
    ocr_text = Column(String, nullable=True)
    ai_extracted_json = Column(JSON, nullable=True)

    observations = Column(String, nullable=True)
    payload_json = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)