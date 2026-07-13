import json
import os

import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:admin@localhost:5672/")
JOBS_QUEUE_NAME = "speech_ai_jobs"


def publish_job(job_id: str, product_slug: str) -> None:
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    try:
        channel = connection.channel()
        channel.queue_declare(queue=JOBS_QUEUE_NAME, durable=True)

        message = json.dumps({"job_id": job_id, "product_slug": product_slug})
        channel.basic_publish(
            exchange="",
            routing_key=JOBS_QUEUE_NAME,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
    finally:
        connection.close()
