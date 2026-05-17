from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.audit_service import log_action
from app.services.auth_service import create_user, validate_driver_assignment

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return db.query(User).order_by(User.created_at.desc()).all()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    payload: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = create_user(
        db,
        email=payload.email,
        full_name=payload.full_name,
        password=payload.password,
        role=payload.role,
        driver_id=payload.driver_id,
    )
    log_action(
        db,
        action="USER_CREATED",
        resource_type="user",
        resource_id=str(user.id),
        user=current_user,
        metadata={"role": user.role, "email": user.email},
        ip_address=request.client.host if request.client else None,
    )
    return user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "ADMIN" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found.")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found.")

    updates = payload.model_dump(exclude_unset=True)
    next_role = updates.get("role", user.role)
    next_driver_id = updates.get("driver_id", user.driver_id)
    validate_driver_assignment(db, role=next_role, driver_id=next_driver_id)

    for key, value in updates.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=UserResponse)
def deactivate_user(
    user_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found.")

    user.is_active = False
    db.commit()
    db.refresh(user)
    log_action(
        db,
        action="USER_DEACTIVATED",
        resource_type="user",
        resource_id=str(user.id),
        user=current_user,
        metadata={"email": user.email},
        ip_address=request.client.host if request.client else None,
    )
    return user
