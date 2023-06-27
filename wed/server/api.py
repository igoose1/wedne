from datetime import datetime, timedelta

import fastapi
import pydantic

from wed.server.commands import CommandSchema, PreciseCommandSchema
from wed.server.db import VisitDAO
from wed.server.settings import settings
from wed.server.tasks import create_new_visit

app = fastapi.FastAPI()


class VisitInputSchema(pydantic.BaseModel):
    social_media_id: int


@app.post("/")
def take_a_visit(
    data: VisitInputSchema,
    dao: VisitDAO = fastapi.Depends(),
) -> PreciseCommandSchema | None:
    now = datetime.utcnow()
    create_new_visit(
        time=now,
        social_media_id=data.social_media_id,
    )
    raw_command = dao.get_command(
        from_=now - timedelta(seconds=settings.seconds_of_delay),
        social_media_id=data.social_media_id,
    )
    if raw_command is None:
        return None
    command = CommandSchema.parse_obj(raw_command)
    return PreciseCommandSchema(
        expected_in=command.when - now,
        **command.dict(),
    )
