import asyncio
import datetime
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from functools import singledispatchmethod
from importlib import metadata

import httpx

from wedne.commands import CommandSchema
from wedne.utils import Backoffer


@dataclass
class Watcher:
    endpoint: str
    delay: datetime.timedelta
    social_media_id: int
    command_processor: Callable[[CommandSchema | None], Awaitable[None]]

    def __post_init__(self) -> None:
        self.backoffer = Backoffer()

    async def __call__(self) -> None:
        version = metadata.version("wedne")
        client = httpx.AsyncClient(
            headers={"user-agent": f"wedne.client/{version}"},
            timeout=10,
        )
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
                await asyncio.sleep(self.delay.seconds)
            except httpx.ConnectError as exc:
                await self.process(exc)
                await asyncio.sleep(self.backoffer.failed())

    @singledispatchmethod
    async def process(self, response: httpx.Response) -> None:
        print(response)
        print(response.content)

        if response.is_server_error:
            print("Server error")
            await asyncio.sleep(self.backoffer.failed())
            return

        if response.is_client_error:
            print("Client error, update me")
            await asyncio.sleep(self.backoffer.failed())
            return

        self.backoffer.succeeded()

        raw_command = response.json()
        command = CommandSchema.parse_obj(raw_command) if raw_command else None
        await self.command_processor(command)

    @process.register
    async def _(self, exception: httpx.ConnectError) -> None:
        print(str(exception))
