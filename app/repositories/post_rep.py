from dataclasses import asdict

from app.database.models import Post
from app.database.db import CustomDatabase
from app.database.schemas import PostDataclass


class PostsRepository:
    def __init__(self, db: CustomDatabase) -> None:
        self.db = db

    async def get(self, data: PostDataclass):
        query = Post.select().where(Post.c.channel == data.channel).filter(Post.c.post_id == data.post_id)
        post_db = await self.db.fetch_one(query)
        if post_db is None:
            return None

        new_data = PostDataclass(
            channel=post_db.channel,
            post_id=post_db.post_id,
            last_id_comm=post_db.last_id_comm
        )
        return new_data

    async def add(self, data: PostDataclass):
        query = Post.insert()
        await self.db.execute(query=query, values=asdict(data))
        return data

    async def upsert(self, data: PostDataclass):
        post = await self.get(data)
        if post is None:
            return await self.add(data)
        return await self.update(data)
        

    async def update(self, data: PostDataclass):
        query = Post.update().where(Post.c.channel == data.channel).filter(Post.c.post_id == data.post_id)
        await self.db.execute(query=query, values=asdict(data))
        return data

    async def delete(self, data: PostDataclass):
        query = Post.delete().where(Post.c.channel == data.channel).filter(Post.c.post_id == data.post_id)
        await self.db.execute(query=query)