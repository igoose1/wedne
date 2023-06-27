import fire
import uvicorn

from wed.server.settings import settings


def main() -> None:
    """
    Server entrypoint

    It's configured with environment variables or .env file."""
    uvicorn.run(
        "wed.server.api:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    fire.core.Display = lambda lines, out: out.write("\n".join(lines) + "\n")  # type: ignore
    fire.Fire(main, name="wed.server")
