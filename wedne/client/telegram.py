import asyncio
import datetime

import pytz
import telethon

from wedne.client.consts import WRITE_FIRST_DELAY
from wedne.client.shared_commands import SharedCommand
from wedne.commands import CommandSchema


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
        await event.respond(command.letter)
        await shared_command.clear()

    return handler


class ChatMonitor:
    def __init__(self, client: telethon.TelegramClient, shared_command: SharedCommand):
        self.client = client
        self.shared_command = shared_command

    async def __call__(self, chat_id: int) -> None:
        self.client.add_event_handler(
            callback=get_handler(self.shared_command),
            event=telethon.events.NewMessage(
                chats=[chat_id],
                incoming=True,
                forwards=False,
            ),
        )


class TelegramTowerBuilder:
    def __init__(self, session: str, api_id: int, api_hash: str, chat_id: int):
        self.client = telethon.TelegramClient(
            session,
            api_id,
            api_hash,
        )
        self.chat_id = chat_id
        self.shared_command = SharedCommand()

    async def start(self) -> None:
        await self.client.start()  # type: ignore

    async def who_am_i(self) -> int:
        return (await self.client.get_me()).id  # type: ignore

    async def monitor(self) -> None:
        await ChatMonitor(self.client, self.shared_command)(
            self.chat_id,
        )

    async def process_command(self, command: CommandSchema | None):
        if command is None:
            await self.shared_command.clear()
            return
        await asyncio.sleep(
            (command.when - datetime.datetime.now(pytz.utc)).seconds,
        )
        if command.after is None:
            # if it's the first letter, wait here and write a message
            await asyncio.sleep(WRITE_FIRST_DELAY.seconds)
            await self.client.send_message(self.chat_id, command.letter)
        else:
            # or wait for a necessary message in ChatMonitor
            await self.shared_command.write(command)
