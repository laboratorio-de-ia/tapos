from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.auth import router as auth_router
from app.routes.subscriptions import router as subscriptions_router
from app.routes.products import router as products_router

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(subscriptions_router)
app.include_router(products_router)

app.mount(
    "/ui",
    StaticFiles(directory=Path(__file__).parent / "static", html=True),
    name="ui",
)
