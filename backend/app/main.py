from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.auth_routes import router as auth_router
from app.api.routes import router
from app.api.review_routes import router as review_router
from app.api.user_routes import router as user_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.services.evidence_service import UPLOADS_ROOT, ensure_evidence_dir

from app.models.store import Store
from app.models.driver import Driver
from app.models.delivery_event import DeliveryEvent
from app.models.order_state import OrderState
from app.models.user import User
from app.models.audit_log import AuditLog


Base.metadata.create_all(bind=engine)
ensure_evidence_dir()

app = FastAPI(
    title="AI Logix API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.cors_origins.split(",")
        if origin.strip()
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOADS_ROOT), name="uploads")

app.include_router(router, prefix="/api")
app.include_router(review_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
