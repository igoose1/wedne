from collections.abc import Callable, Hashable, Iterable, Sequence
from typing import TypeVar

T_ = TypeVar("T_")


def distinct_on(seq: Iterable[T_], key: Callable[[T_], Hashable]) -> Sequence[T_]:
    unique = {key(element): element for element in seq}
    return list(unique.values())


class Backoffer:
    def __init__(self, base: float = 2, max_value: float = 32):
        self.base = base
        self.max_value = max_value
        self.counter = 0

    def failed(self) -> float:
        result = min(self.max_value, self.base**self.counter)
        self.counter += 1
        return result

    def succeeded(self) -> None:
        self.counter = 0
