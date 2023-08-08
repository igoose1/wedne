import random
from datetime import datetime, timedelta

import huey
import pytz

from wedne.commands import CommandSchema
from wedne.server.db import VisitDAO, VisitModel
from wedne.server.settings import settings
from wedne.utils import distinct_on

job_queue = huey.SqliteHuey(filename=settings.job_queue_database)


@job_queue.task(priority=10)
def create_new_visit(time: datetime, social_media_id: int) -> None:
    dao = VisitDAO()
    dao.create(time, social_media_id)


def choose_randoms_to_order(dao: VisitDAO) -> list[VisitModel]:
    """Raises ValueError if there are not sufficient candidates."""
    active = dao.get_from(
        datetime.now(pytz.utc) - timedelta(minutes=settings.minutes_of_last_activity),
    )
    return random.sample(
        distinct_on(active, lambda vis: vis.social_media_id),
        k=len(settings.tower),
    )


@job_queue.periodic_task(
    huey.crontab(minute=f"*/{settings.minutes_to_order}", strict=True),
    priority=20,
)
def order_new_commands() -> None:
    dao = VisitDAO()
    previous_social_media_id = None
    try:
        chosen = choose_randoms_to_order(dao)
    except ValueError:
        raise
    when = datetime.now(pytz.utc) + timedelta(seconds=settings.seconds_of_delay)
    for idx, letter in enumerate(settings.tower):
        command = CommandSchema(
            letter=letter,
            after=previous_social_media_id,
            when=when,
        )
        dao.update_command(chosen[idx].id, command.dict())
        previous_social_media_id = chosen[idx].social_media_id
