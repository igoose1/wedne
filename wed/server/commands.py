import datetime
from typing import Annotated

import pydantic


class CommandSchema(pydantic.BaseModel):
    letter: Annotated[str, pydantic.constr(min_length=1, max_length=1)]
    after: int | None = pydantic.Field(
        description="social_media_id user before current command",
    )
    when: datetime.datetime
