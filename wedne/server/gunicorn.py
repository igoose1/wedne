# Gunicorn configuration

from wedne.server.settings import settings

bind = f"{settings.host}:{settings.port}"
workers = settings.workers
worker_class = "uvicorn.workers.UvicornWorker"
