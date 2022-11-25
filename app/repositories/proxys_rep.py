import socks

from app.database.models import Proxy
from app.database.db import CustomDatabase


class ProxysRepositrory:
    def __init__(self, db: CustomDatabase) -> None:
        self.db = db

    async def get_all(self):
        query = Proxy.select()
        proxys_db = await self.db.fetch_all(query)
        if proxys_db != []:
            proxys = []
            for proxy in proxys_db:
                proxys.append((socks.SOCKS5, proxy.addr, proxy.port, True, proxy.login, proxy.password))
            return proxys
        return None

    
    async def add(self, data: dict):
        query = Proxy.insert()
        await self.db.execute(query=query, values=data)
        return data