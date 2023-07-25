import asyncio
import datetime

import pytz
import telethon

from wed.client.consts import WRITE_FIRST_DELAY
from wed.client.shared_commands import SharedCommand
from wed.commands import CommandSchema


def get_handler(shared_command: SharedCommand):
    async def handler(event: telethon.events.NewMessage.Event) -> None:
        print(event)
        print(f"got new {type(event)}, btw, my task is", await shared_command.read())
        command = await shared_command.read()
        if command is None:
            # no pending command
            print("no pending")
            return
        if command.when > datetime.datetime.now(pytz.utc):
            # it's too early by time
            print("too early by time")
            return
        if command.after is not None and command.after != event.from_id.user_id:
            # it's still early by letter order
            print("too early by letter order")
            return
        await event.reply(command.letter)
        await shared_command.clear()

    return handler


class ChatMonitor:
    def __init__(self, client: telethon.TelegramClient, shared_command: SharedCommand):
        self._client = client
        self._shared_command = shared_command

    async def __call__(self, chat_id: int) -> None:
        self._client.add_event_handler(
            callback=get_handler(self._shared_command),
            event=telethon.events.NewMessage(
                chats=[chat_id],
                incoming=True,
                forwards=False,
            ),
        )


class TelegramTowerBuilder:
    def __init__(self, session: str, api_id: int, api_hash: str, chat_id: int):
        self._client = telethon.TelegramClient(
            session,
            api_id,
            api_hash,
        )
        self._chat_id = chat_id
        self._shared_command = SharedCommand()
        self._who_am_i_cache: int | None = None

    async def start(self) -> None:
        await self._client.start()  # type: ignore

    async def who_am_i(self) -> int:
        return (await self._client.get_me()).id  # type: ignore

    async def monitor(self) -> None:
        await self.who_am_i()
        await ChatMonitor(self._client, self._shared_command)(
            self._chat_id,
        )

    async def process_command(self, command: CommandSchema):
        if command.after is None:
            # if it's the first letter, wait here and write a message
            await asyncio.sleep(
                (command.when - datetime.datetime.now(pytz.utc)).seconds,
            )
            await asyncio.sleep(WRITE_FIRST_DELAY.seconds)
            await self._client.send_message(self._chat_id, command.letter)
        else:
            # or wait for a necessary message in ChatMonitor
            await self._shared_command.write(command)
