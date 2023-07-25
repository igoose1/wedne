import ctypes
import multiprocessing

from wed.commands import CommandSchema

COMMAND_LENGTH = 256  # we assume json's length of CommandSchema is less than 256


class SharedCommand:
    def __init__(self):
        self.__lock = multiprocessing.Lock()
        self.__array = multiprocessing.Array(
            ctypes.c_char,
            COMMAND_LENGTH,
        )

    def write(self, command: CommandSchema) -> None:
        with self.__lock:
            self.__array.value = command.json().encode()  # type: ignore

    def clear(self) -> None:
        with self.__lock:
            self.__array.value = b""  # type: ignore

    def read(self) -> CommandSchema | None:
        with self.__lock:
            if not self.__array.value:  # type: ignore
                return None
            return CommandSchema.parse_raw(self.__array.value)  # type: ignore
