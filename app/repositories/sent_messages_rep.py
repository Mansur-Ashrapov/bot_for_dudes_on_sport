from dataclasses import asdict

from app.database.models import SentMessages
from app.database.db import CustomDatabase
from app.database.schemas import SentMessagesDataclassOut, SentMessagesDataclassIn


class SentMessagesRepository:
    def __init__(self, db: CustomDatabase) -> None:
        self.db = db

    async def get(self, data: SentMessagesDataclassIn):
        query = SentMessages.select().where(SentMessages.c.from_client == data.from_client).filter(SentMessages.c.participant_id == data.participant_id)
        sent_message_db = await self.db.fetch_one(query)
        if sent_message_db is None:
            return None

        new_data = SentMessagesDataclassOut(
            from_client=sent_message_db.from_client,
            participant_id=sent_message_db.participant_id,
            sent_date=sent_message_db.sent_date
        )
        return new_data

    async def get_by_participant_id(self, data: SentMessagesDataclassIn):
        query = SentMessages.select().where(SentMessages.c.participant_id == data.participant_id)
        sent_message_db = await self.db.fetch_one(query)
        if sent_message_db is None:
            return None

        new_data = SentMessagesDataclassOut(
            from_client=sent_message_db.from_client,
            participant_id=sent_message_db.participant_id,
            sent_date=sent_message_db.sent_date
        )
        return new_data

    async def add(self, data: SentMessagesDataclassIn):
        query = SentMessages.insert()
        await self.db.execute(query=query, values=asdict(data))
        return data

    async def upsert(self, data: SentMessagesDataclassIn):
        sent_message = await self.get(data)
        if sent_message is None:
            return await self.add(data)
        return await self.update(data)
        

    async def update(self, data: SentMessagesDataclassIn):
        query = SentMessages.select().where(SentMessages.c.from_client == data.from_client).filter(SentMessages.c.participant_id == data.participant_id)
        await self.db.execute(query=query, values=asdict(data))
        return data

    async def delete(self, data: SentMessagesDataclassIn):
        query = SentMessages.select().where(SentMessages.c.from_client == data.from_client).filter(SentMessages.c.participant_id == data.participant_id)
        await self.db.execute(query=query)