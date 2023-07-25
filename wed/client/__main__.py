import multiprocessing
import os
import signal

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
        self_id_receiver, self_id_sender = multiprocessing.Pipe(duplex=False)
        monitor_process = multiprocessing.Process(
            target=telegram_tower_builder.monitor,
            args=(self_id_sender,),
        )
        try:
            monitor_process.start()
            watcher = Watcher(
                endpoint,
                seconds_of_delay=seconds_of_delay,
                social_media_id=self_id_receiver.recv(),
                command_processor=telegram_tower_builder.process_command,
            )
            watcher()
        except KeyboardInterrupt:
            if monitor_process.pid is not None:
                print("interrupt a process")
                os.kill(monitor_process.pid, signal.SIGINT)
                monitor_process.join(timeout=10)
        finally:
            if monitor_process.is_alive():
                print("terminate a process")
                monitor_process.terminate()


if __name__ == "__main__":
    fire.core.Display = lambda lines, out: out.write(  # type: ignore
        "\n".join(lines) + "\n",
    )
    fire.Fire(Main(), name="wed.client")
