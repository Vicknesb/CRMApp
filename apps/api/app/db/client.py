from prisma import Prisma

_client: Prisma | None = None


async def get_db() -> Prisma:
    if _client is None or not _client.is_connected():
        raise RuntimeError("Prisma client not connected")
    return _client


async def connect() -> None:
    global _client
    _client = Prisma()
    await _client.connect()


async def disconnect() -> None:
    global _client
    if _client and _client.is_connected():
        await _client.disconnect()
