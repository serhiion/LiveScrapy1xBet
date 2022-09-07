import json
import aioredis


async def get_redis_client():
    return aioredis.Redis(host='localhost', port=6379, db=0)


async def write_dict_to_redis(data: list):
    db: aioredis.Redis = await get_redis_client()

    for pk, football in enumerate(data):
        await db.set(pk, json.dumps(football))


async def get_all_date_from_redis():
    db: aioredis.Redis = await get_redis_client()

    finally_info = list()
    for key in await db.keys('*'):
        finally_info.append(await db.get(key))

    return finally_info
