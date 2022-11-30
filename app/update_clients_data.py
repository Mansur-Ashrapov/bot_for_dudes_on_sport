import json

import app.config as config

from dependency_injector.wiring import Provide, inject

from app.database.schemas import TelegramClientDataclass
from app.container import AppContainer
from app.repositories import (
    TelegramClientRepository,
    ProxysRepositrory
)


@inject
async def update_clients_data(tg_clients_rep: TelegramClientRepository = Provide[AppContainer.tg_clients_rep], proxys_rep: ProxysRepositrory = Provide[AppContainer.proxys_repo]): 
    clients = get_data_from_json(config.CLIENTS_USERNAMES)
    if clients != []:
        for client in clients:
            client_db = await tg_clients_rep.get(client.username)
            if client_db is None:
                # clients_db = await tg_clients_rep.get_all()
                # free_proxy = await choose_free_proxy(clients_db, proxys_db)
                # client.proxy_id = free_proxy
                await tg_clients_rep.add(client)


# @inject
# async def choose_free_proxy(clients_db, proxys_db: dict):
#     ids_db = [key for key, items in proxys_db.items()]
#     try:
#         proxys_used = [client.proxy_id for client in clients_db]
#     except TypeError:
#         return int(ids_db[0])

#     for id in ids_db:
#         if int(id) not in proxys_used:
#             return int(id)


def get_data_from_json(usernames: list[str]) -> list[TelegramClientDataclass]:
    result = []
    for username in usernames:
        try:
            with open(f'{username}.json', 'r') as file:
                data = json.loads(file.read())
                result.append(TelegramClientDataclass(
                    username=username,
                    api_hash=str(data['app_hash']),
                    api_id=str(data['app_id']),
                ))
        except FileNotFoundError:
            continue
    return result