import random
from collections.abc import Callable, Hashable, Iterable, Sequence
from datetime import datetime, timedelta
from typing import TypeVar

import huey

from wed.commands import CommandSchema
from wed.server.db import VisitDAO, VisitModel
from wed.server.settings import settings

job_queue = huey.SqliteHuey(settings.job_queue_database)


@job_queue.task()
def create_new_visit(time: datetime, social_media_id: int) -> None:
    dao = VisitDAO()
    dao.create(time, social_media_id)


T_ = TypeVar("T_")


def distinct_on(seq: Iterable[T_], key: Callable[[T_], Hashable]) -> Sequence[T_]:
    unique: dict[Hashable, T_] = {key(element): element for element in seq}
    return list(unique.values())


def choose_randoms_to_order(dao: VisitDAO) -> list[VisitModel]:
    """Raises ValueError if there are not sufficient candidates."""
    active = dao.get_from(
        datetime.utcnow() - timedelta(minutes=settings.minutes_of_last_activity),
    )
    return random.sample(
        distinct_on(active, lambda vis: vis.social_media_id),
        k=len(settings.tower),
    )


@job_queue.periodic_task(
    huey.crontab(minute=f"*/{settings.minutes_to_order}", strict=True),
)
def order_new_commands() -> None:
    dao = VisitDAO()
    previous_social_media_id = None
    try:
        chosen = choose_randoms_to_order(dao)
    except ValueError:
        raise
    when = datetime.utcnow() + timedelta(seconds=settings.seconds_of_delay)
    for idx, letter in enumerate(settings.tower):
        command = CommandSchema(
            letter=letter,
            after=previous_social_media_id,
            when=when,
        )
        dao.update_command(chosen[idx].id, command.dict())
        previous_social_media_id = chosen[idx].social_media_id
