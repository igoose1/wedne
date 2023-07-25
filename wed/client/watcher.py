import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import singledispatchmethod
from importlib import metadata

import httpx

from wed.commands import CommandSchema


@dataclass
class Watcher:
    endpoint: str
    seconds_of_delay: int
    social_media_id: int
    command_processor: Callable[[CommandSchema], None]

    def __post_init__(self) -> None:
        version = metadata.version("wed")
        self.client = httpx.Client(headers={"user-agent": f"wed.client/{version}"})

    def __call__(self) -> None:
        data = {
            "social_media_id": self.social_media_id,
        }
        while True:
            try:
                response = self.client.post(
                    self.endpoint,
                    json=data,
                )
                self.process(response)
            except httpx.ConnectError as exc:
                self.process(exc)
            time.sleep(self.seconds_of_delay)

    @singledispatchmethod
    def process(self, response: httpx.Response) -> None:
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
        self.command_processor(command)  # there's time.sleep

    @process.register
    def _(self, exception: httpx.ConnectError) -> None:
        print(str(exception))
