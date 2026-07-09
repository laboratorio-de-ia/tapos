cd /workspace/tecle/platform/saas-backend
source .venv/bin/activate

export DATABASE_URL=postgresql+psycopg2://admin:admin@localhost:5432/platform
export SECRET_KEY="tapos-dev-secret-key"

uvicorn app.main:app --reload