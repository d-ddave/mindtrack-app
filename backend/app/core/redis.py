import redis.asyncio as aioredis

from app.core.config import settings

redis_client = aioredis.from_url(
    settings.UPSTASH_REDIS_URL,
    password=settings.UPSTASH_REDIS_TOKEN,
    decode_responses=True,
    ssl=True,
)


async def get_redis() -> aioredis.Redis:
    return redis_client
