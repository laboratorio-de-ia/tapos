from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.models import User, Product, Subscription
from app.products.speech_ai_adapter import run_speech_ai_product

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).all()


@router.get("/{product_slug}/access")
def product_access(
    product_slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.slug == product_slug).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.product_id == product.id,
        Subscription.is_active == True
    ).first()

    if not subscription:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "product_slug": product_slug,
        "access": True
    }


@router.post("/speech-ai/run")
def run_speech_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.slug == "speech-ai").first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.product_id == product.id,
        Subscription.is_active == True
    ).first()

    if not subscription:
        raise HTTPException(status_code=403, detail="Access denied")

    result = run_speech_ai_product()
    return result
