from dataclasses import asdict

from app.database.models import TelegramClient
from app.database.db import CustomDatabase
from app.database.schemas import TelegramClientDataclass

class TelegramClientRepository:
    def __init__(self, db: CustomDatabase) -> None:
        self.db = db

    async def get(self, username: str):
        query = TelegramClient.select().where(TelegramClient.c.username == username)
        client_db = await self.db.fetch_one(query)
        result = client_db
        if client_db is not None:
            result = TelegramClientDataclass(
                username=username,
                api_hash=client_db.api_hash,
                api_id=client_db.api_id,
                proxy_id=client_db.proxy_id
            )
        return result

    
    async def get_all(self) -> list[TelegramClientDataclass]:
        query = TelegramClient.select()
        client_db = await self.db.fetch_all(query)
        result = []
        
        if client_db != []:
            for client in client_db:
                result.append(TelegramClientDataclass(
                    username=client.username,
                    api_hash=client.api_hash,
                    api_id=client.api_id,
                    proxy_id=client.proxy_id
                ))
            return result
        return None


    async def add(self, data: TelegramClientDataclass):
        query = TelegramClient.insert()
        await self.db.execute(query=query, values=asdict(data))

    async def upsert(self, data: TelegramClientDataclass):
        post = await self.get(data)
        if post is None:
            await self.add(data)
        else:
            await self.update(data)

    async def update(self, data: TelegramClientDataclass):
        data_db = await self.get(data)
        data.count_new_users_post += data_db.count_new_users_post
        query = TelegramClient.update().where(TelegramClient.c.username == data.username)
        await self.db.execute(query=query, values=asdict(data))

    async def delete(self, username: str):
        query = TelegramClient.delete().where(TelegramClient.c.username == username)
        await self.db.execute(query=query)