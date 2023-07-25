import multiprocessing

import fire

from wed.client.telegram import TelegramTowerBuilder
from wed.client.telegram_creds import API_HASH, API_ID
from wed.client.watcher import Watcher


class Main:
    def __call__(
        self,
        endpoint: str,
        seconds_of_delay: int = 2,
        chat_id: int = -984039342,
    ) -> None:
        telegram_tower_builder = TelegramTowerBuilder(
            "wed",
            API_ID,
            API_HASH,
            chat_id,
        )
        watcher = Watcher(
            endpoint,
            seconds_of_delay=seconds_of_delay,
            social_media_id=telegram_tower_builder.whoami(),
            command_processor=telegram_tower_builder.process_command,
        )
        monitor_process = multiprocessing.Process(
            target=telegram_tower_builder.monitor,
        )
        try:
            monitor_process.start()
            watcher()
        except KeyboardInterrupt:
            print("bye!")
        finally:
            monitor_process.terminate()


if __name__ == "__main__":
    fire.core.Display = lambda lines, out: out.write(  # type: ignore
        "\n".join(lines) + "\n",
    )
    fire.Fire(Main(), name="wed.client")
