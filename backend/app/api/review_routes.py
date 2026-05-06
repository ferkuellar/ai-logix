from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.dependencies import require_supervisor_or_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.review import (
    HumanConfirmRequest,
    HumanRejectRequest,
    HumanReviewResponse,
    ReviewDetailResponse,
    ReviewPendingResponse,
)
from app.services.review_service import (
    confirm_review,
    get_review_detail,
    list_pending_reviews,
    reject_review,
    serialize_review_event,
)
from app.services.audit_service import log_action

router = APIRouter(prefix="/review", tags=["human-review"])


@router.get("/pending", response_model=list[ReviewPendingResponse])
def read_pending_reviews(
    status: Optional[str] = None,
    order_number: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    _: User = Depends(require_supervisor_or_admin),
):
    return list_pending_reviews(
        db,
        status_filter=status,
        order_number=order_number,
        limit=limit,
        offset=offset,
    )


@router.get("/{event_id}", response_model=ReviewDetailResponse)
def read_review_detail(
    event_id: UUID,
    db: Session = Depends(get_db),
    _: User = Depends(require_supervisor_or_admin),
):
    return get_review_detail(db, event_id)


@router.post("/{event_id}/confirm", response_model=HumanReviewResponse)
def confirm_human_review(
    event_id: UUID,
    payload: HumanConfirmRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisor_or_admin),
):
    event = confirm_review(db, event_id, payload.model_dump())
    data = serialize_review_event(event)["ai_extracted_json"]
    log_action(
        db,
        action="HUMAN_REVIEW_CONFIRMED",
        resource_type="delivery_event",
        resource_id=str(event.id),
        user=current_user,
        metadata={"order_number": event.order_number, "status": event.status},
        ip_address=request.client.host if request.client else None,
    )

    return {
        "event_id": event.id,
        "review_status": data["review_status"],
        "confirmed": True,
        "ai_extracted_json": data,
    }


@router.post("/{event_id}/reject", response_model=HumanReviewResponse)
def reject_human_review(
    event_id: UUID,
    payload: HumanRejectRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_supervisor_or_admin),
):
    event = reject_review(db, event_id, payload.model_dump())
    data = serialize_review_event(event)["ai_extracted_json"]
    log_action(
        db,
        action="HUMAN_REVIEW_REJECTED",
        resource_type="delivery_event",
        resource_id=str(event.id),
        user=current_user,
        metadata={"reason": payload.reason},
        ip_address=request.client.host if request.client else None,
    )

    return {
        "event_id": event.id,
        "review_status": data["review_status"],
        "confirmed": False,
        "ai_extracted_json": data,
    }
