# Gunicorn configuration

from wedne.server.settings import settings

bind = f"{settings.host}:{settings.port}"
workers = settings.workers
threads = 4
worker_class = "uvicorn.workers.UvicornWorker"
