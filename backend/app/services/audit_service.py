from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.user import User


def log_action(
    db: Session,
    *,
    action: str,
    resource_type: str,
    user: User | None = None,
    user_id: UUID | None = None,
    resource_id: str | None = None,
    metadata: dict | None = None,
    ip_address: str | None = None,
) -> AuditLog:
    audit_log = AuditLog(
        user_id=user.id if user else user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        metadata_json=metadata,
        ip_address=ip_address,
    )
    db.add(audit_log)
    db.commit()
    return audit_log
