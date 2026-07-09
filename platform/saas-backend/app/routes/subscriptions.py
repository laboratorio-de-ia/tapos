from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import Product, Subscription, User

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])


class SubscriptionRequest(BaseModel):
    product_slug: str


def _serialize(subscription: Subscription) -> dict:
    return {
        "id": subscription.id,
        "product_id": subscription.product_id,
        "product_slug": subscription.product.slug,
        "is_active": subscription.is_active,
        "created_at": subscription.created_at,
    }


@router.post("")
def create_subscription(
    data: SubscriptionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.slug == data.product_slug).first()
    if not product or not product.is_active:
        raise HTTPException(status_code=404, detail="Product not found")

    subscription = Subscription(user_id=current_user.id, product_id=product.id)
    db.add(subscription)
    db.commit()
    db.refresh(subscription)

    return _serialize(subscription)


@router.get("")
def list_subscriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    subscriptions = (
        db.query(Subscription).filter(Subscription.user_id == current_user.id).all()
    )
    return [_serialize(subscription) for subscription in subscriptions]
