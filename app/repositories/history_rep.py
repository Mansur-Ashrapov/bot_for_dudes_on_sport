from dataclasses import asdict

from app.database.models import History
from app.database.db import CustomDatabase
from app.database.schemas import PostHistoryDataclassIn, PostHistoryDataclassOut

class HistoryRepository:
    def __init__(self, db: CustomDatabase) -> None:
        self.db = db

    async def get(self, data: PostHistoryDataclassIn):
        query = History.select().where(History.c.channel == data.channel).filter(History.c.post_id == data.post_id)
        post_db = await self.db.fetch_one(query)
        if post_db is not None:
            new_data = PostHistoryDataclassOut(
                channel=post_db.channel,
                post_id=post_db.post_id,
                count_new_users_post=post_db.count_new_users_post,
                last_check_date=post_db.last_check_date
            )
            return new_data
        return None

    async def add(self, data: PostHistoryDataclassIn):
        query = History.insert()
        await self.db.execute(query=query, values=asdict(data))

    async def upsert(self, data: PostHistoryDataclassIn):
        post = await self.get(data)
        if post is None:
            await self.add(data)
        else:
            await self.update(data)

    async def update(self, data: PostHistoryDataclassIn):
        data_db = await self.get(data)
        data.count_new_users_post += data_db.count_new_users_post
        query = History.update().where(History.c.channel == data.channel).filter(History.c.post_id == data.post_id)
        await self.db.execute(query=query, values=asdict(data))

    async def delete(self, data: PostHistoryDataclassIn):
        query = History.delete().where(History.c.channel == data.channel).filter(History.c.post_id == data.post_id)
        await self.db.execute(query=query)