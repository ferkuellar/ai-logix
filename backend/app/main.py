from fastapi import FastAPI

from app.api.routes import router
from app.db.base import Base
from app.db.session import engine

from app.models.store import Store
from app.models.driver import Driver
from app.models.delivery_event import DeliveryEvent
from app.models.order_state import OrderState


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Logix API",
    version="0.1.0"
)

app.include_router(router, prefix="/api")