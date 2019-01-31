import os
import ssl
import asyncpg
import random
import pytz


def random_color():
    return int('0x' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]), 0)


def get_utc_string(dt):
    return dt.astimezone(pytz.utc).strftime("%d %b %Y %H:%M %Z")


async def connect_to_db():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    return await asyncpg.connect(dsn=os.environ.get("DATABASE_URL"), ssl=ssl_ctx)
