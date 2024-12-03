import os
import pytz
import aiohttp
import asyncpg
import random as r


def random_color():
    return int('0x' + ''.join([r.choice('0123456789ABCDEF') for _ in range(6)]), 0)


def get_utc_string(dt):
    return dt.astimezone(pytz.utc).strftime("%d %b %Y %H:%M %Z")

async def connect_to_db():
    return await asyncpg.connect(dsn=os.environ.get("DATABASE_URL"))


async def get_json_data(url, content_type='application/json'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json(content_type=content_type)
