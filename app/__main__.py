import asyncio
import logging
import schedule
import socks
import time
import random

import config

from telethon.sessions import SQLiteSession
from telethon.sync import TelegramClient
from dependency_injector.wiring import Provide, inject

from app.repositories import ProxysRepositrory
from app.config import USERNAME
from app.database.db import CustomDatabase
from app.container import AppContainer
from app.jobs import (
    collect_users,
    send_invites_to_users
)


logging.basicConfig()
logging.getLogger('telethon').setLevel(logging.DEBUG)


# Один аккаунт становится базовым, Arica ты уже сделал админом, так что он и базовый
base_client = None
clients = {}

#Сюда нужно вписать данные аккаунтов
clients_data = [
    {'api_id': '', 'api_hash': '', 'username': ''}
]

def job(loop, func, **kwargs):
    loop.run_until_complete(start_clients())
    loop.run_until_complete(func(**kwargs))
    loop.run_until_complete(disconnect_clients())


@inject
async def start_up(db: CustomDatabase = Provide[AppContainer.db]):
    await db.connect()


@inject
async def start_clients(proxys_repo: ProxysRepositrory = Provide[AppContainer.proxys_repo]):
    proxys = await proxys_repo.get_all()

    random.shuffle(proxys)

    session = SQLiteSession(session_id=config.USERNAME)
    client = TelegramClient(
        session=session,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        proxy=proxys[0]
    )
    base_client = client
    await base_client.connect()

    
    prx_number = 1
    for data in clients_data:
        session = SQLiteSession(data['username'])
        cl = TelegramClient(session, data['api_id'], data['api_hash'], proxy=proxys[prx_number])
        await cl.connect()
        clients[data['username']] = cl
        prx_number += 1


async def disconnect_clients():
    await base_client.disconnect()
    for name, client in clients.items():
        await client.disconnect()


if __name__ == '__main__': 
    container = AppContainer()
    container.wire(modules=[__name__, 'app'])
    
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_up())

    schedule.every().day.at('00:00').do(job, func=collect_users, loop=loop, client=base_client)
    schedule.every(4).days.at('03:00').do(job, func=send_invites_to_users, loop=loop, clients=clients)

    while True:
        schedule.run_pending()
        print(schedule.get_jobs())
        time.sleep(1)