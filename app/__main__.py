import asyncio
import logging
import schedule
import socks
import time
import random

import app.config as config

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
from app.update_clients_data import update_clients_data
from app.update_proxys_data import update_proxys


logging.basicConfig()
logging.getLogger('telethon').setLevel(logging.DEBUG)



def job(loop, func, on_startup, **kwargs):
    if on_startup is not None:
        loop.run_until_complete(on_startup())
    loop.run_until_complete(func(**kwargs))

@inject
async def db_connect(db: CustomDatabase = Provide[AppContainer.db]):
    await db.connect()

async def start_up():
    await db_connect()
    proxys = await update_proxys()
    await update_clients_data(proxys)


if __name__ == '__main__': 
    container = AppContainer()
    container.wire(modules=[__name__, 'app'])
    
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_up())

    schedule.every(5).seconds.do(job, func=collect_users, loop=loop)
    # schedule.every().day.at('00:00').do(job, func=collect_users, loop=loop)
    # schedule.every(4).days.at('03:00').do(job, func=send_invites_to_users, loop=loop)

    while True:
        schedule.run_pending()
        print(schedule.get_jobs())
        time.sleep(1)