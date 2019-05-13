import os
import ssl
import pytz
import aiohttp
import asyncpg
import random as r


def random_color():
    return int('0x' + ''.join([r.choice('0123456789ABCDEF') for _ in range(6)]), 0)


def get_utc_string(dt):
    return dt.astimezone(pytz.utc).strftime("%d %b %Y %H:%M %Z")


def create_ssl():
    """Probably redundant, docs say that True can be passed to create default cert"""
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    return ssl_ctx


async def connect_to_db():
    return await asyncpg.connect(dsn=os.environ.get("DATABASE_URL"), ssl=create_ssl())


async def get_json_data(url, content_type='application/json'):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json(content_type=content_type)
