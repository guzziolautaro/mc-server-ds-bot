import aiohttp
import asyncio

class MinecraftNetworkError(Exception):
    """Custom exception for Minecraft bridge errors"""
    def __init__(self, status, message):
        self.status = status
        self.message = message

class NetworkManager:
    def __init__(self):
        self.session = None

    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def send_request(self, ip: str, port: int, token: str, action: str, params: dict = None):
        url = f"http://{ip}:{port}/bot"
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {"action": action}
        if params:
            payload.update(params)

        session = await self.get_session()
        
        try:
            async with session.post(url, json=payload, headers=headers, timeout=5) as resp:
                if resp.status == 200:
                    return await resp.text()
                elif resp.status == 403:
                    raise MinecraftNetworkError(403, "Invalid Token")
                else:
                    raise MinecraftNetworkError(resp.status, f"HTTP Error {resp.status}")
        except aiohttp.ClientConnectorError:
            raise MinecraftNetworkError(503, "Could not connect to the server")
        except asyncio.TimeoutError:
            raise MinecraftNetworkError(408, "Server timed out")
        
    async def close(self):
        if self.session:
            await self.session.close()
    
