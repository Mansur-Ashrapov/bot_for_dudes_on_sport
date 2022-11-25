from dataclasses import asdict

from app.database.models import User
from app.database.db import CustomDatabase
from app.database.schemas import UserDataclass


class UserRepository:
    def __init__(self, db: CustomDatabase) -> None:
        self.db = db

    async def get(self, data: UserDataclass):
        query = User.select().where(User.c.user_id == data.user_id)
        user_db = await self.db.fetch_one(query)
        if user_db is not None:
            new_data = UserDataclass(
                user_id=user_db.user_id
            )
            return new_data
        return None

    async def add(self, data: UserDataclass):
        query = User.insert()
        await self.db.execute(query=query, values=asdict(data))

    async def upsert(self, data: UserDataclass):
        User = await self.get(data)
        if User is None:
            await self.add(data)
        else:
            await self.update(data)

    async def update(self, data: UserDataclass):
        query = User.update().where(User.c.user_id == data.user_id)
        await self.db.execute(query=query, values=asdict(data))

    async def delete(self, data: UserDataclass):
        query = User.delete().where(User.c.user_id == data.user_id)
        await self.db.execute(query=query)