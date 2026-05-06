from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import oauth2_scheme
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import get_user_by_id


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except JWTError as exc:
        raise credentials_error from exc

    user = get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise credentials_error
    return user


def require_roles(*allowed_roles: str) -> Callable:
    allowed = {role.upper() for role in allowed_roles}

    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )
        return current_user

    return dependency


require_admin = require_roles("ADMIN")
require_supervisor_or_admin = require_roles("ADMIN", "SUPERVISOR")
require_driver_or_above = require_roles("ADMIN", "SUPERVISOR", "DRIVER")
