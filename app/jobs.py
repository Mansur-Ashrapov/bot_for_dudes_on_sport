from dependency_injector.wiring import Provide, inject
from telethon.sync import TelegramClient

from app.container import AppContainer
from app.login_collector import LoginCollector
from app.invites_sendler import InvitesSendler
from app.repositories import (
    UserRepository,
)
from app.database.schemas import UserDataclass


@inject
async def collect_users(client, login_collector: LoginCollector = Provide[AppContainer.login_collector]):

    # тут добавляешь каналы с которых собирать посты
    channels = ['https://t.me/victorblud']
    await login_collector.collect_users(channels=channels, client=client)


@inject
async def send_invites_to_users(clients: dict, invates_sendler: InvitesSendler = Provide[AppContainer.invites_sendler]):
    
    channel_url = '\n@on_sport_dudes'
    # Сообщения, к ним атоматом добавляется url группы на новой строке
    messages = [
        'Подписывайтесь на наш канал',
        'Мы ведем спортивный канал',
        'Приглашаем посмотреть за нашим прогрессом',
    ]
    messages = [mess + channel_url for mess in messages]

    for name, client in clients.items():
        await invates_sendler.send_invites(client=client, client_phone=int(name), count=10, messages=messages)
    