import asyncio

from telethon.sync import TelegramClient, errors

from app.database.schemas import (
    PostDataclass,
    PostHistoryDataclassIn,
    NewUserDataclassIn,
    UserDataclass
)
from app.repositories import (
    UserRepository,
    NewUserRepository,
    HistoryRepository,
    PostsRepository
)


class LoginCollector:
    def __init__(self, client: TelegramClient, new_users_repo: NewUserRepository, users_repo: UserRepository, posts_repo: PostsRepository, history_repo: HistoryRepository) -> None:
        self.new_users_repo = new_users_repo
        self.users_repo = users_repo 
        self.posts_repo = posts_repo
        self.history_repo = history_repo
        self.client = client
        # self.channels_repo = channels_repo


    async def collect_users(self, channels):
        await self.client.connect()
        
        try:
            await self._update_group_participants()
            for channel in channels:
                messages = await self.client.get_messages(channel, limit=10)
                for message in messages:
                    message_db = await self.posts_repo.get(PostDataclass(channel, message.id, 0))
                    
                    last_id_comm = await self._get_last_comm_id(channel, message.id)
                    last_id_comm_db = message_db.last_id_comm if message_db is not None else 0
                    if last_id_comm > last_id_comm_db:
                        try:
                            count_new_users_post = await self._collect_users_from_post(channel, message.id, last_id_comm_db)
                            await self.posts_repo.upsert(PostDataclass(channel, message.id, last_id_comm))
                            await self.history_repo.upsert(PostHistoryDataclassIn(channel, message.id, count_new_users_post))
                        except errors.MsgIdInvalidError:
                            continue
                    else:
                        await self.history_repo.upsert(PostHistoryDataclassIn(channel, message.id, 0))
        finally:    
            await self.client.disconnect()

    async def _collect_users_from_post(self, channel, message_id, last_id):
        count_new_users_post = 0
        async for comm in self.client.iter_messages(channel, reply_to=message_id, offset_id=last_id):
            try:
                sender_id = comm.from_id.user_id
            except AttributeError:
                continue
            user_in_current_users = await self.users_repo.get(UserDataclass(sender_id))
            user_in_new_users = await self.new_users_repo.get(NewUserDataclassIn(sender_id, None, None, None))
            if user_in_current_users is None and user_in_new_users is None:
                username = await self._get_username(sender_id)
                await self.new_users_repo.add(NewUserDataclassIn(user_id=sender_id, username=username, channel_from=channel, post_id=message_id))
                count_new_users_post += 1
        return count_new_users_post


    async def _get_last_comm_id(self, channel, id):
        id = None
        async for comm in self.client.iter_messages(channel, reply_to=id, limit=1):
            return comm.id
    

    async def _get_username(self, user_id):
        user = await self.client.get_entity(user_id)
        return user.username
    

    async def _update_group_participants(self):
        participants = await self.client.get_participants('https://t.me/on_sport_dudes')
        for participant in participants:
            user = await self.users_repo.get(UserDataclass(participant.id))
            if user is None:
                await self.users_repo.add(UserDataclass(participant.id))


