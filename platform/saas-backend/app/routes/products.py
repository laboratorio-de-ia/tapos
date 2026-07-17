import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user
from app.jobs.publisher import publish_job
from app.jobs.schemas import JobSubmitResponse
from app.models import EditalAnalise, Job, User, Product, Subscription
from app.products.speech_ai_adapter import run_speech_ai_product
from app.products.code_ai_adapter import run_code_ai_product
from app.products.edital_ai_adapter import (
    arquivar_processado,
    find_current_edital_file,
    run_edital_ai_product,
)

router = APIRouter(prefix="/products", tags=["products"])

SPEECH_AI_INPUT_FILE = Path("/workspace/tecle/products/speech-ai/input/script.txt")

CODE_AI_INPUT_DIR = Path("/workspace/tecle/products/code-ai/input")
CODE_AI_ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".doc", ".xlsx", ".xls", ".csv",
    ".pptx", ".ppt", ".png", ".jpg", ".jpeg", ".txt", ".md",
}

EDITAL_AI_INPUT_DIR = Path("/workspace/tecle/products/edital-ai/input")
EDITAL_AI_ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt", ".md"}
EDITAL_AI_DOWNLOAD_FORMATS = {"excel", "pdf", "word", "email"}


def _require_active_subscription(
    db: Session, current_user: User, product_slug: str
) -> Product:
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

    return product


def _submit_job(
    db: Session, current_user: User, product_slug: str
) -> JobSubmitResponse:
    _require_active_subscription(db, current_user, product_slug)

    job = Job(
        job_id=str(uuid.uuid4()),
        user_id=current_user.id,
        product_slug=product_slug,
        status="queued",
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    publish_job(job_id=job.job_id, product_slug=job.product_slug)

    return JobSubmitResponse(
        job_id=job.job_id, status=job.status, product_slug=job.product_slug
    )


def _persist_edital_analise(
    db: Session, current_user: User, result: dict, job_id: str = None
) -> EditalAnalise:
    analise = EditalAnalise(
        analise_id=result["edital_id"],
        user_id=current_user.id,
        job_id=job_id,
        numero_edital=result.get("numero_edital"),
        orgao=result.get("orgao"),
        modalidade=result.get("modalidade"),
        score_conformidade=result.get("score_conformidade"),
        resumo_executivo=result.get("resumo_executivo"),
        arquivos_gerados=result.get("arquivos_gerados"),
        result_json=result,
    )
    db.add(analise)
    db.commit()
    db.refresh(analise)
    return analise


@router.get("")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).all()


@router.get("/{product_slug}/access")
def product_access(
    product_slug: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, product_slug)

    return {
        "product_slug": product_slug,
        "access": True
    }


@router.post("/speech-ai/run")
def run_speech_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "speech-ai")

    result = run_speech_ai_product()
    return result


@router.post("/speech-ai/submit", response_model=JobSubmitResponse)
def submit_speech_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _submit_job(db, current_user, "speech-ai")


@router.post("/speech-ai/upload")
async def upload_speech_ai_source(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "speech-ai")

    content = await file.read()
    SPEECH_AI_INPUT_FILE.write_bytes(content)

    result = run_speech_ai_product()
    return result


@router.post("/code-ai/run")
def run_code_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "code-ai")

    result = run_code_ai_product()
    return result


@router.post("/code-ai/submit", response_model=JobSubmitResponse)
def submit_code_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _submit_job(db, current_user, "code-ai")


@router.post("/code-ai/upload")
async def upload_code_ai_source(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "code-ai")

    extension = Path(file.filename).suffix.lower()
    if extension not in CODE_AI_ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail=f"Formato não suportado: {extension}"
        )

    CODE_AI_INPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = CODE_AI_INPUT_DIR / f"documento{extension}"

    content = await file.read()
    destination.write_bytes(content)

    result = run_code_ai_product(input_file=str(destination))
    return result


@router.post("/edital-ai/run")
def run_edital_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "edital-ai")

    atual = find_current_edital_file()
    if atual is None:
        raise HTTPException(
            status_code=400,
            detail="Nenhum edital enviado ainda. Use /products/edital-ai/upload primeiro.",
        )

    result = run_edital_ai_product(input_file=str(atual))
    _persist_edital_analise(db, current_user, result)
    arquivar_processado(atual)
    return result


@router.post("/edital-ai/submit", response_model=JobSubmitResponse)
def submit_edital_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "edital-ai")

    if find_current_edital_file() is None:
        raise HTTPException(
            status_code=400,
            detail="Nenhum edital enviado ainda. Use /products/edital-ai/upload primeiro.",
        )

    return _submit_job(db, current_user, "edital-ai")


@router.post("/edital-ai/upload")
async def upload_edital_ai_source(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "edital-ai")

    extension = Path(file.filename).suffix.lower()
    if extension not in EDITAL_AI_ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, detail=f"Formato não suportado: {extension}"
        )

    EDITAL_AI_INPUT_DIR.mkdir(parents=True, exist_ok=True)
    for antigo in EDITAL_AI_INPUT_DIR.iterdir():
        if antigo.is_file():
            antigo.unlink()

    # mantém o nome original do arquivo enviado (só o nome, sem diretórios,
    # para evitar path traversal) para que os artefatos gerados e o arquivo
    # arquivado em processados/ sejam identificáveis pelo mesmo nome do
    # documento carregado do início ao fim do fluxo
    nome_arquivo = Path(file.filename).name
    destination = EDITAL_AI_INPUT_DIR / nome_arquivo
    content = await file.read()
    destination.write_bytes(content)

    result = run_edital_ai_product(input_file=str(destination))
    _persist_edital_analise(db, current_user, result)
    arquivar_processado(destination, nome_original=file.filename)
    return result


@router.get("/edital-ai/historico")
def historico_edital_ai(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "edital-ai")

    analises = (
        db.query(EditalAnalise)
        .filter(EditalAnalise.user_id == current_user.id)
        .order_by(EditalAnalise.created_at.desc())
        .all()
    )

    return [
        {
            "analise_id": a.analise_id,
            "numero_edital": a.numero_edital,
            "orgao": a.orgao,
            "modalidade": a.modalidade,
            "score_conformidade": a.score_conformidade,
            "created_at": a.created_at,
        }
        for a in analises
    ]


@router.get("/edital-ai/download/{analise_id}")
def download_edital_ai_artefato(
    analise_id: str,
    formato: str = "excel",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _require_active_subscription(db, current_user, "edital-ai")

    if formato not in EDITAL_AI_DOWNLOAD_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato inválido. Use um de: {sorted(EDITAL_AI_DOWNLOAD_FORMATS)}",
        )

    analise = (
        db.query(EditalAnalise)
        .filter(
            EditalAnalise.analise_id == analise_id,
            EditalAnalise.user_id == current_user.id,
        )
        .first()
    )
    if not analise:
        raise HTTPException(status_code=404, detail="Análise não encontrada")

    caminho = (analise.arquivos_gerados or {}).get(formato)
    if not caminho or not Path(caminho).exists():
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    return FileResponse(caminho, filename=Path(caminho).name)
