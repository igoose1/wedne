import asyncio

from wedne.commands import CommandSchema


class SharedCommand:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._command: CommandSchema | None = None

    async def write(self, command: CommandSchema) -> None:
        async with self._lock:
            self._command = command

    async def clear(self) -> None:
        async with self._lock:
            self._command = None

    async def read(self) -> CommandSchema | None:
        async with self._lock:
            return self._command
