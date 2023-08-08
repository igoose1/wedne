import asyncio

import aiorun
import fire

from wedne.client.consts import API_HASH, API_ID, WATCHING_DELAY
from wedne.client.telegram import TelegramTowerBuilder
from wedne.client.watcher import Watcher


async def main(
    endpoint: str,
    chat_id: int,
) -> None:
    telegram_tower_builder = TelegramTowerBuilder(
        "wedne",
        API_ID,
        API_HASH,
        chat_id,
    )
    await telegram_tower_builder.start()
    monitor_task = asyncio.create_task(telegram_tower_builder.monitor())
    watcher = Watcher(
        endpoint,
        delay=WATCHING_DELAY,
        social_media_id=await telegram_tower_builder.who_am_i(),
        command_processor=telegram_tower_builder.process_command,
    )
    watcher_task = asyncio.create_task(watcher())
    await asyncio.wait(
        [
            monitor_task,
            watcher_task,
        ],
    )


def sync_main(
    endpoint: str,
    chat_id: int = -984039342,
) -> None:
    aiorun.run(main(endpoint, chat_id), stop_on_unhandled_errors=True)


if __name__ == "__main__":
    fire.core.Display = lambda lines, out: out.write(  # type: ignore
        "\n".join(lines) + "\n",
    )
    fire.Fire(sync_main, name="wedne.client")
