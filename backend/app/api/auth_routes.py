from fastapi import APIRouter, Depends, Request, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import CurrentUserResponse, LoginRequest, TokenResponse
from app.services.audit_service import log_action
from app.services.auth_service import authenticate_user, create_access_token, get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        existing_user = get_user_by_email(db, payload.email)
        log_action(
            db,
            action="LOGIN_FAILED",
            resource_type="auth",
            user_id=existing_user.id if existing_user else None,
            metadata={"email": payload.email},
            ip_address=request.client.host if request.client else None,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    log_action(
        db,
        action="LOGIN_SUCCESS",
        resource_type="auth",
        user=user,
        ip_address=request.client.host if request.client else None,
    )

    return {"access_token": create_access_token(user.id), "token_type": "bearer"}


@router.get("/me", response_model=CurrentUserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user
