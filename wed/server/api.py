import datetime

import fastapi
import pydantic

from wed.server.db import VisitDAO
from wed.server.tasks import create_new_visit

app = fastapi.FastAPI()


class VisitInputSchema(pydantic.BaseModel):
    social_media_id: int


@app.post("/")
def take_a_visit(
    data: VisitInputSchema,
    dao: VisitDAO = fastapi.Depends(),
) -> None:
    create_new_visit(
        time=datetime.datetime.utcnow(),
        social_media_id=data.social_media_id,
    )
