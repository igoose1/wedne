from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    minutes_to_order: int
    seconds_of_delay: int
    minutes_of_last_activity: int
    app_database: Path
    job_queue_database: Path
    tower: str = "ITSWEDNESDAYMYDUDES"
    host: str
    port: int
    reload: bool = False
    model_config = SettingsConfigDict(env_file=".env", env_prefix="wedne_")


settings = Settings()  # type: ignore
