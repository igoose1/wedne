import multiprocessing
from pathlib import Path

from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    minutes_to_order: int
    seconds_of_delay: int
    minutes_of_last_activity: int
    app_database: Path
    redis: RedisDsn
    tower: str = "ITSWEDNESDAYMYDUDES"
    host: str
    port: int
    reload: bool = False
    workers: int = multiprocessing.cpu_count() * 2
    model_config = SettingsConfigDict(env_file=".env", env_prefix="wedne_")


settings = Settings()  # type: ignore
