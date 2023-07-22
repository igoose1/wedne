import time
from datetime import datetime
from typing import Any

from wed.commands import CommandSchema


class Executor:
    def __init__(self, raw: dict[str, Any]):
        self.command = CommandSchema.parse_obj(raw)

    def __call__(self) -> None:
        time.sleep((self.command.when - datetime.utcnow()).seconds)
        if self.command.after is None:
            print("FIRE!!")
            print("ops, wrong, not a letter")
            print(self.command.letter)
        else:
            print("waiting a correct message in Telegram")
            print(...)
