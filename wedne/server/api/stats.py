from datetime import datetime, timedelta

import fastapi
import pydantic
import pytz

from wedne.server.db import VisitDAO
from wedne.server.settings import settings
from wedne.utils import distinct_on

router = fastapi.APIRouter()


class StatSchema(pydantic.BaseModel):
    duration: timedelta
    visits: int
    unique_visits: int


@router.get("/")
def get_statistics(
    dao: VisitDAO = fastapi.Depends(),
) -> StatSchema:
    duration = timedelta(minutes=settings.minutes_of_last_activity)
    active = dao.get_from(
        datetime.now(pytz.utc) - duration,
    )
    unique = distinct_on(active, lambda vis: vis.social_media_id)
    return StatSchema(
        duration=duration,
        visits=len(active),
        unique_visits=len(unique),
    )
