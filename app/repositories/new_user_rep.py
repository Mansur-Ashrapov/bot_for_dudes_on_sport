from dataclasses import asdict

from app.database.models import NewUser
from app.database.db import CustomDatabase
from app.database.schemas import NewUserDataclassIn, NewUserDataclassOut

class NewUserRepository:
    def __init__(self, db: CustomDatabase) -> None:
        self.db = db

    async def get(self, data: NewUserDataclassIn):
        query = NewUser.select().where(NewUser.c.user_id == data.user_id)
        new_user_db = await self.db.fetch_one(query)
        if new_user_db is not None:
            new_data = NewUserDataclassOut(
                user_id=new_user_db.user_id,
                add_date=new_user_db.add_date,
                username=new_user_db.username,
                channel_from=new_user_db.channel_from,
                post_id=new_user_db.post_id
            )
            return new_data
        return None
    
    async def get_all(self):
        query = NewUser.select()
        new_user_db = await self.db.fetch_all(query)
        if new_user_db != []:
            new_users = []
            for u in new_user_db:
                new_users.append(NewUserDataclassOut(
                    user_id=u.user_id,
                    add_date=u.add_date,
                    username=u.username,
                    channel_from=u.channel_from,
                    post_id=u.post_id
            ))
            return new_users
        return None

    async def add(self, data: NewUserDataclassIn):
        query = NewUser.insert()
        await self.db.execute(query=query, values=asdict(data))

    async def upsert(self, data: NewUserDataclassIn):
        NewUser = await self.get(data)
        if NewUser is None:
            await self.add(data)
        else:
            await self.update(data)

    async def update(self, data: NewUserDataclassIn):
        query = NewUser.update().where(NewUser.c.user_id == data.user_id)
        await self.db.execute(query=query, values=asdict(data))

    async def delete(self, data: NewUserDataclassIn):
        query = NewUser.delete().where(NewUser.c.user_id == data.user_id)
        await self.db.execute(query=query)