import json
import os

import pika

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:admin@localhost:5672/")

QUEUE_NAMES = {
    "speech-ai": "speech_ai_jobs",
    "code-ai": "code_ai_jobs",
    "edital-ai": "edital_ai_jobs",
}


def publish_job(job_id: str, product_slug: str) -> None:
    queue_name = QUEUE_NAMES[product_slug]

    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    try:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)

        message = json.dumps({"job_id": job_id, "product_slug": product_slug})
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2),
        )
    finally:
        connection.close()
