from aiohttp import ClientSession
from ujson import loads

class Parser:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = None

    # запрос
    async def get(self, url):
        if self.session is None:
            self.session = ClientSession(base_url=self.base_url)
        async with self.session.get(url) as response:
            return await response.json(loads=loads)

    async def get_address(self, address):
        json = await self.get(f'/api/address/{address}')
        print(f'funded_txo_count: {json["chain_stats"]["funded_txo_count"]}')

    async def get_address_transactions(self, address):
        json = await self.get(f'/api/address/{address}/txs')
        print(f'block_hash: {json[0]["status"]["block_hash"]}')

    async def get_block(self, hash):
        json = await self.get(f'/api/block/{hash}')
        print(f'bits: {json["bits"]}')

    async def get_mining_pools(self):
        json = await self.get('/api/v1/mining/pools/1w')
        print(f'poolId: {json["pools"][0]["poolId"]}')

    async def get_mempool(self):
        json = await self.get('/api/mempool')
        print(f'count: {json["count"]}')

    # закрытие сессии
    async def close_session(self):
        if self.session is not None:
            await self.session.close()


async def main():
    parse_session = Parser(base_url='https://mempool.space') 
    await parse_session.get_mining_pools()

    await parse_session.close_session()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
