import redis.asyncio as redis
import json

"""creating a connection pool to Redis
    coonnecting the application to the Redis server"""

async def get_redis_server():
    return await redis.from_url(
        "redis://localhost:6379",
        encoding = "utf-8",
        decode_responses = True
    )

"""add store and retrieve functions to cache data in Redis"""




# create cache data
async def cache_set(key:str, value, expires:int=60):
    redis_server = await get_redis_server()

    await redis_server.set(key, json.dumps(value), ex=expires)
    await redis_server.close()

# retrieving cached data from redis 
async def cache_get(key:str):
    redis_server = await get_redis_server()
    data = await redis_server.get(key)
    await redis_server.close()

    return json.loads(data) if data else None


