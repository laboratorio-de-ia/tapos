import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.jobs.publisher import publish_job
from app.jobs.schemas import JobSubmitResponse
from app.models import Job, User, Product, Subscription
from app.products.speech_ai_adapter import run_speech_ai_product

router = APIRouter(prefix="/products", tags=["products"])

SPEECH_AI_INPUT_FILE = Path("/workspace/tecle/products/speech-ai/input/script.txt")


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


@router.post("/speech-ai/submit", response_model=JobSubmitResponse)
def submit_speech_ai(
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

    job = Job(
        job_id=str(uuid.uuid4()),
        user_id=current_user.id,
        product_slug="speech-ai",
        status="queued",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    publish_job(job_id=job.job_id, product_slug=job.product_slug)

    return JobSubmitResponse(
        job_id=job.job_id, status=job.status, product_slug=job.product_slug
    )


@router.post("/speech-ai/upload")
async def upload_speech_ai_source(
    file: UploadFile = File(...),
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

    content = await file.read()
    SPEECH_AI_INPUT_FILE.write_bytes(content)

    result = run_speech_ai_product()
    return result
