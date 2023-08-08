import logging

import fire
import uvicorn
from huey.consumer_options import ConsumerConfig

from wedne.server.settings import settings
from wedne.server.tasks import job_queue


class Main:
    """
    Server for tower building

    Everything is configured with environment variables or .env file.
    """

    def run_api(self) -> None:
        """
        Server entrypoint
        """
        uvicorn.run(
            "wedne.server.api:app",
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
        )

    def consume_tasks(self) -> None:
        """
        Run Huey Consumer

        It's a task executor which is used for almost everything.
        """
        config = ConsumerConfig(
            workers=1,
            periodic=True,
            max_delay=2.0,
        )
        logger = logging.getLogger("huey")
        config.setup_logger(logger)

        consumer = job_queue.create_consumer(**config.values)
        consumer.run()


if __name__ == "__main__":
    fire.core.Display = lambda lines, out: out.write(  # type: ignore
        "\n".join(lines) + "\n",
    )
    fire.Fire(Main(), name="wedne.server")
