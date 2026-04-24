import os

from celery import Celery

redis_url = os.getenv("UPSTASH_REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "mindtrack",
    broker=redis_url,
    backend=redis_url,
    include=["app.tasks.reminder_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    broker_use_ssl={
        "ssl_cert_reqs": "CERT_NONE",
    },
)
