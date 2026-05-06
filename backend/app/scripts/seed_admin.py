from app.core.config import settings
from app.db.base import Base
from app.db.session import SessionLocal
from app.db.session import engine
from app.models.audit_log import AuditLog
from app.models.delivery_event import DeliveryEvent
from app.models.driver import Driver
from app.models.order_state import OrderState
from app.models.store import Store
from app.models.user import User
from app.services.auth_service import create_user, get_user_by_email


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = get_user_by_email(db, settings.seed_admin_email)
        if existing:
            print(f"Admin user already exists: {existing.email}")
            return

        user = create_user(
            db,
            email=settings.seed_admin_email,
            full_name=settings.seed_admin_name,
            password=settings.seed_admin_password,
            role="ADMIN",
        )
        print(f"Admin user created: {user.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
