from dependency_injector.wiring import Provide, inject
from telethon.sync import TelegramClient
from telethon.sessions import SQLiteSession

from app.container import AppContainer
from app.login_collector import LoginCollector
from app.invites_sendler import InvitesSendler
from app.repositories import (
    TelegramClientRepository,
    ProxysRepositrory
)
from app.get_proxies import get_free_proxies


@inject
async def collect_users(login_collector: LoginCollector = Provide[AppContainer.login_collector]):

    # тут добавляешь каналы с которых собирать посты
    channels = ['https://t.me/victorblud']
    await login_collector.collect_users(channels=channels)


@inject
async def send_invites_to_users(invates_sendler: InvitesSendler = Provide[AppContainer.invites_sendler], tg_clients_rep: TelegramClientRepository = Provide[AppContainer.tg_clients_rep]):
    
    # Сообщения, к ним атоматом добавляется url группы на новой строке
    messages = [
        '\nМы ведем спортивный канал, заходи к нам',
        '\nПриглашаем посмотреть за нашим спортивным прогрессом',
        '\nУ нас можно наблюдать за спортивным прогрессом сильных людей',
        '\nПриглашаем к нам на канал спортивного контента',
        '\nЗаходи на наш канал спортивного движа)',
    ]
    
    clients = await tg_clients_rep.get_all()
    
    for client_data in clients:
        session = SQLiteSession(client_data.username)
        proxy = get_free_proxies()
        client = TelegramClient(session, client_data.api_id, client_data.api_hash, proxy=proxy)
        await invates_sendler.send_invites(client=client, client_phone=client_data.username, count=5, messages=messages)
    