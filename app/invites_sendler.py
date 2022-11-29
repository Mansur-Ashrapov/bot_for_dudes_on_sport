import random
import time

from telethon.sync import TelegramClient, errors

from app.repositories import (
    UserRepository,
    NewUserRepository,
    SentMessagesRepository
)
from app.database.schemas import SentMessagesDataclassIn


class InvitesSendler:

    def __init__(self, users_repo: UserRepository, new_users_repo: NewUserRepository, sent_messages_repo: SentMessagesRepository) -> None:
        self.users_repo = users_repo
        self.new_users_repo = new_users_repo
        self.sent_messages_repo = sent_messages_repo


    async def send_invites(self, client: TelegramClient, client_phone: str, count: int, messages: list):
        await client.connect()

        channel_urls = ['\n@on_sport_dudes', '\nhttps://t.me/on_sport_dudes']
        hello_messages = ['Привет!', 'Доброго времени суток!', 'Приветствую!', 'Йоу!', 'Здарова!', 'Хай)', 'Привет)', 'Здарова)']

        try:
            new_users = await self._get_not_used_users()
            for user in new_users:
                if count == 0:
                    break
                mess = random.choice(hello_messages) + random.choice(messages) + random.choice(channel_urls)

                try:
                    # По другому нельзя сделать, необходимо "найти" человека в коментариях и тогда можно будет отправить ему сообщение
                    async for message in client.iter_messages(user.channel_from, reply_to=user.post_id):
                        if message.from_id.user_id == user.user_id:
                            u = await client.get_entity(user.user_id)
                            await client.send_message(u, mess)
                            await self.sent_messages_repo.add(SentMessagesDataclassIn(
                                from_client=client_phone,
                                participant_id=user.user_id
                            ))
                            count -= 1
                            time.sleep(random.randint(30, 60))
                            break
                except errors.PeerFloodError:
                    break
        finally:
            await client.disconnect()


    async def _get_not_used_users(self):
        new_users = await self.new_users_repo.get_all()
        res = []
        for u in new_users:
            user_is_used = await self.sent_messages_repo.get_by_participant_id(SentMessagesDataclassIn(participant_id=u.user_id, from_client=None))
            if user_is_used is None:
                res.append(u)
        return res
