import typing

from sqlalchemy import (
    create_engine,
    MetaData
)
from databases import Database, DatabaseURL


metadata = MetaData()


class CustomDatabase(Database):
    def __init__(self, url: typing.Union[str, "DatabaseURL"], *, force_rollback: bool = False, **options: typing.Any):
        super().__init__(url, force_rollback=force_rollback, **options)
        self._db_url = url
        self._engine = create_engine(url, echo=True)
        self.create_database()

    def create_database(self) -> None:
        metadata.create_all(self._engine)
