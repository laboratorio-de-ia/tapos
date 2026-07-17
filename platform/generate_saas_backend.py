import os
import zipfile

BASE_DIR = "saas-backend-base"

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)

# -------------------------
# Criar estrutura
# -------------------------

files = {

"README.md": """# SaaS Backend Tecle
Backend base FastAPI para plataforma SaaS com JWT, usuários, produtos e assinaturas.
""",

".env.example": """DATABASE_URL=postgresql+psycopg2://admin:admin@postgres:5432/platform
SECRET_KEY=supersecret
""",

"requirements.txt": """fastapi
uvicorn
sqlalchemy
psycopg2-binary
python-jose
passlib[bcrypt]
pydantic
""",

"Dockerfile": """FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
""",

"docker-compose.app.yml": """services:
  saas-backend:
    build: .
    container_name: saas-backend
    ports:
      - "8000:8000"
    networks:
      - core_net

networks:
  core_net:
    external: true
""",

"app/main.py": """from fastapi import FastAPI
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
""",

"init_db.py": """print("init ok")"""

}

# -------------------------
# Criar arquivos
# -------------------------

for file, content in files.items():
    write_file(os.path.join(BASE_DIR, file), content)

# -------------------------
# Criar ZIP
# -------------------------

zip_name = "saas-backend-base.zip"

with zipfile.ZipFile(zip_name, "w") as z:
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            path = os.path.join(root, file)
            z.write(path, path)

print(f"ZIP gerado: {zip_name}")
``
