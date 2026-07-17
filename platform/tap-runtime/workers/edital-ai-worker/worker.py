import json
import os
import sys

import pika
import psycopg2

SAAS_BACKEND_ROOT = os.getenv(
    "SAAS_BACKEND_ROOT", "/workspace/tecle/platform/saas-backend"
)
sys.path.insert(0, SAAS_BACKEND_ROOT)

from app.products.edital_ai_adapter import (  # noqa: E402
    arquivar_processado,
    find_current_edital_file,
    run_edital_ai_product,
)

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin:admin@localhost:5432/platform"
)
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:admin@localhost:5672/")
JOBS_QUEUE_NAME = "edital_ai_jobs"


def _connect_db():
    dsn = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql://")
    return psycopg2.connect(dsn)


def _mark_running(job_id: str) -> None:
    with _connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE jobs SET status = %s, started_at = now() WHERE job_id = %s",
                ("running", job_id),
            )


def _mark_completed(job_id: str, result: dict) -> None:
    with _connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE jobs SET status = %s, finished_at = now(), result_json = %s "
                "WHERE job_id = %s",
                ("completed", json.dumps(result), job_id),
            )


def _mark_failed(job_id: str, error_message: str) -> None:
    with _connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE jobs SET status = %s, finished_at = now(), error_message = %s "
                "WHERE job_id = %s",
                ("failed", error_message, job_id),
            )


def _get_user_id(job_id: str) -> int:
    with _connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id FROM jobs WHERE job_id = %s", (job_id,))
            row = cur.fetchone()
            return row[0]


def _persist_analise(user_id: int, job_id: str, result: dict) -> None:
    with _connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO edital_analises
                    (analise_id, user_id, job_id, numero_edital, orgao, modalidade,
                     score_conformidade, resumo_executivo, arquivos_gerados,
                     result_json, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
                ON CONFLICT (analise_id) DO NOTHING
                """,
                (
                    result["edital_id"],
                    user_id,
                    job_id,
                    result.get("numero_edital"),
                    result.get("orgao"),
                    result.get("modalidade"),
                    result.get("score_conformidade"),
                    result.get("resumo_executivo"),
                    json.dumps(result.get("arquivos_gerados")),
                    json.dumps(result),
                ),
            )


def process_message(job_id: str, product_slug: str) -> None:
    _mark_running(job_id)
    try:
        atual = find_current_edital_file()
        result = run_edital_ai_product(input_file=str(atual) if atual else None)
        user_id = _get_user_id(job_id)
        _persist_analise(user_id, job_id, result)
        _mark_completed(job_id, result)
        if atual:
            arquivar_processado(atual)
    except Exception as exc:  # noqa: BLE001
        _mark_failed(job_id, str(exc))


def on_message(channel, method, properties, body):
    payload = json.loads(body)
    process_message(payload["job_id"], payload["product_slug"])
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue=JOBS_QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=JOBS_QUEUE_NAME, on_message_callback=on_message)

    print("edital-ai-worker: aguardando jobs...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
