import json
import os

import pika
import psycopg2

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin:admin@localhost:5432/platform"
)
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:admin@localhost:5672/")
JOBS_QUEUE_NAME = "speech_ai_jobs"


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


def process_message(job_id: str, product_slug: str) -> None:
    _mark_running(job_id)
    try:
        result = {"status": "executed", "product_slug": product_slug}
        _mark_completed(job_id, result)
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

    print("speech-ai-worker: aguardando jobs...")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
