from redis.asyncio import Redis


def create_redis(dsn: str) -> Redis:
    return Redis.from_url(dsn, decode_responses=True)