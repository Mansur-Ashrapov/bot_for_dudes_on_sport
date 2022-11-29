from dependency_injector.wiring import Provide, inject

from app.container import AppContainer
from app.repositories import ProxysRepositrory


@inject
async def update_proxys(proxys_rep: ProxysRepositrory = Provide[AppContainer.proxys_repo]):
    new_proxys = get_proxys_from_file('proxies')
    for proxy in new_proxys:
        await proxys_rep.upsert(proxy)
    proxys_db = await proxys_rep.get_all()
    return proxys_db


def get_proxys_from_file(file_name: str) -> list:
    f = open(f'{file_name}.txt','r')
    proxys_data = []
    try:
        lines = f.readlines()
        for line in lines:
            data = line.split(':')
            proxys_data.append({'addr': data[0], 'port': int(data[1]), 'login': data[2], 'password': data[3].replace('\n', '')})
    finally:
        f.close()
    return proxys_data