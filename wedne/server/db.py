import json
from collections.abc import Hashable
from datetime import datetime
from functools import partial
from typing import Any

import peewee
from playhouse.sqlite_ext import JSONField

from wedne.server.settings import settings

database = peewee.SqliteDatabase(settings.app_database, autoconnect=False)


class AutoFieldType(int, peewee.AutoField):
    pass


class JSONFieldType(dict[Hashable, Any], JSONField):
    pass


class VisitModel(peewee.Model):
    id: AutoFieldType = peewee.AutoField(primary_key=True)  # type: ignore
    when: datetime = peewee.DateTimeField(index=True)  # type: ignore
    social_media_id: int = peewee.BigIntegerField()  # type: ignore
    command: JSONFieldType = JSONField(
        json_dumps=partial(json.dumps, default=str),
        null=True,
    )  # type: ignore

    class Meta:
        database = database


class VisitDAO:
    def create(self, time: datetime, social_media_id: int) -> VisitModel:
        with database:
            return VisitModel.create(when=time, social_media_id=social_media_id)

    def update_command(self, id: int, command: dict[str, Any]) -> None:
        with database:
            VisitModel.update(command=command).where(VisitModel.id == id).execute()

    def get_from(self, from_: datetime) -> list[VisitModel]:
        with database:
            return list(VisitModel.select().where(VisitModel.when >= from_))

    def get_command(
        self,
        from_: datetime,
        social_media_id: int,
    ) -> None | dict[str, Any]:
        with database:
            visit: VisitModel | None = (
                VisitModel.select(VisitModel.command)
                .where(VisitModel.social_media_id == social_media_id)
                .where(VisitModel.when >= from_)
                .where(VisitModel.command.is_null(False))
                .get_or_none()
            )
        return None if visit is None else visit.command  # type: ignore

    def get_commanded(self, from_: datetime) -> list[VisitModel]:
        with database:
            return list(
                VisitModel.select()
                .where(VisitModel.when >= from_)
                .where(VisitModel.command.is_null(False)),
            )


with database:
    database.create_tables([VisitModel])
