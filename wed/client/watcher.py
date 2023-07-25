import asyncio
import datetime
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from functools import singledispatchmethod
from importlib import metadata

import httpx

from wed.commands import CommandSchema


@dataclass
class Watcher:
    endpoint: str
    delay: datetime.timedelta
    social_media_id: int
    command_processor: Callable[[CommandSchema], Awaitable[None]]

    async def __call__(self) -> None:
        version = metadata.version("wed")
        client = httpx.AsyncClient(headers={"user-agent": f"wed.client/{version}"})
        try:
            await self._watch(client)
        finally:
            await client.aclose()

    async def _watch(self, client: httpx.AsyncClient) -> None:
        data = {
            "social_media_id": self.social_media_id,
        }
        while True:
            try:
                response = await client.post(
                    self.endpoint,
                    json=data,
                )
                await self.process(response)
            except httpx.ConnectError as exc:
                await self.process(exc)
            await asyncio.sleep(self.delay.seconds)

    @singledispatchmethod
    async def process(self, response: httpx.Response) -> None:
        print(response)
        print(response.content)

        if response.is_server_error:
            print("Server error")
            return

        if response.is_client_error:
            print("Client error, update me")
            return

        raw_command = response.json()
        if raw_command is None:
            return
        command = CommandSchema.parse_obj(raw_command)
        await self.command_processor(command)  # there's time.sleep

    @process.register
    async def _(self, exception: httpx.ConnectError) -> None:
        print(str(exception))
