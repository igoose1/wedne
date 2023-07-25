import datetime
import time

import telethon

from wed.client.shared_commands import SharedCommand
from wed.commands import CommandSchema


def get_handler(shared_command: SharedCommand):
    async def handler(event) -> None:
        print(event)
        command = shared_command.read()
        if command is None:
            # no pending command
            return
        if command.when < datetime.datetime.utcnow():
            # it's too early by time
            return
        if command.after is not None and command.after != await event.from_id:
            # it's still early by letter order
            return
        event.reply(command.letter)
        shared_command.clear()

    return handler


class ChatMonitor:
    def __init__(self, client: telethon.TelegramClient, shared_command: SharedCommand):
        self.__client = client
        self.__shared_command = shared_command

    def __call__(self, chat_id: int) -> None:
        self.__client.add_event_handler(
            callback=get_handler(self.__shared_command),
            event=telethon.events.NewMessage(
                chats=[chat_id],
                incoming=True,
                forwards=False,
            ),
        )
        self.__client.run_until_disconnected()


class TelegramTowerBuilder:
    def __init__(self, session: str, api_id: int, api_hash: str, chat_id: int):
        self.__client = telethon.TelegramClient(
            session,
            api_id,
            api_hash,
        )
        self.__client.start()
        self.__chat_id = chat_id
        self.__shared_command = SharedCommand()

    def whoami(self) -> int:
        me: telethon.types.User = self.__client.loop.run_until_complete(
            self.__client.get_me(),  # type: ignore
        )
        return me.id

    def monitor(self):
        self.__client.start()
        ChatMonitor(self.__client, self.__shared_command)(
            self.__chat_id,
        )

    def process_command(self, command: CommandSchema):
        time.sleep((command.when - datetime.datetime.utcnow()).seconds)
        if command.after is None:
            # if it's the first letter, write a message straightaway
            self.__client.loop.run_until_complete(
                self.__client.send_message(self.__chat_id, command.letter),
            )
        else:
            # or wait for a necessary message in ChatMonitor
            self.__shared_command.write(command)

    def clear(self):
        self.__shared_command.clear()
