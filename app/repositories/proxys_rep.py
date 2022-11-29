import socks

from app.database.models import Proxy
from app.database.db import CustomDatabase


class ProxysRepositrory:
    def __init__(self, db: CustomDatabase) -> None:
        self.db = db


    async def get_by_addr(self, addr):
        query = Proxy.select().where(Proxy.c.addr == addr)
        proxy_db = await self.db.fetch_one(query=query)
        if proxy_db is not None:
            return (socks.SOCKS5, proxy_db.addr, proxy_db.port, True, proxy_db.login, proxy_db.password)
        return None


    async def get_by_id(self, id):
        query = Proxy.select().where(Proxy.c.id == id)
        proxy_db = await self.db.fetch_one(query=query)
        if proxy_db is not None:
            return (socks.SOCKS5, proxy_db.addr, proxy_db.port, True, proxy_db.login, proxy_db.password)
        return None

    async def get_all(self):
        query = Proxy.select()
        proxys_db = await self.db.fetch_all(query)
        if proxys_db != []:
            proxys = {}
            for proxy in proxys_db:
                proxys[f'{proxy.id}'] = (socks.SOCKS5, proxy.addr, proxy.port, True, proxy.login, proxy.password)
            return proxys
        return None

    async def upsert(self, data: dict):
        proxy = await self.get_by_addr(data['addr'])
        if proxy is None:
            return await self.add(data)
        return await self.update(data)
        

    async def update(self, data: dict):
        query = Proxy.update().where(Proxy.c.addr == data['addr'])
        await self.db.execute(query=query, values=data)
        return data
    
    async def add(self, data: dict):
        query = Proxy.insert()
        await self.db.execute(query=query, values=data)
        return data