from collections.abc import Callable, Hashable, Iterable, Sequence
from typing import TypeVar

T_ = TypeVar("T_")


def distinct_on(seq: Iterable[T_], key: Callable[[T_], Hashable]) -> Sequence[T_]:
    unique = {key(element): element for element in seq}
    return list(unique.values())
