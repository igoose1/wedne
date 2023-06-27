import pydantic


class Settings(pydantic.BaseSettings):
    minutes_to_order: int
    seconds_of_delay: int
    minutes_of_last_activity: int
    job_queue_database: str
    tower: str = "ITSWEDNESDAYMYDUDES"
    host: str
    port: int
    reload: bool = False

    class Config:
        env_file = ".env"
        env_prefix = "wed_"


settings = Settings()  # type: ignore
