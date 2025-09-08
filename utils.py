import os
from typing import Any, Optional
import pytz
import aiohttp
import asyncpg
import random as r
import re
import discord
import datetime as dt


sunday_image_url: str = "https://fixvx.com/notnoe_/status/1964794280469540951"
weekday_image_url: str = "https://tenor.com/view/uma-uma-musume-musume-marvelous-sunday-marvelous-gif-15092128582077845004"

def random_color() -> int:
    return int('0x' + ''.join([r.choice('0123456789ABCDEF') for _ in range(6)]), 0)


def get_utc_string(datetime: dt.datetime) -> str:
    return datetime.astimezone(pytz.utc).strftime("%d %b %Y %H:%M %Z")

async def connect_to_db() -> asyncpg.Connection:
    dsn = os.environ.get("DATABASE_URL")
    return await asyncpg.connect(dsn=dsn)


async def get_json_data(url: str, content_type: str = 'application/json') -> Any:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json(content_type=content_type)

def process_message_replies(message: discord.Message) -> Optional[str]:
    out: Optional[str] = None
    content_lower = message.content.lower()
    if "/o/" in content_lower:
        out = "\\o\\"
    elif "\\o\\" in content_lower:
        out = "/o/"
    elif re.search(r"(^|\W)(ay{2,})($|\W)", content_lower) is not None:
        out = "LMAO" if "AYY" in message.content else "lmao"
    elif "\\o/" in content_lower:
        out = "\\o/"
    elif re.search(r"(^|\W)(owo)($|\W)", content_lower) is not None:
        if r.randint(1, 100) <= 20:
            out = r.choice(["kys", "uwu", "o3o", " *nuzzles wuzzles*", "no", "Rawr xD", "·///·"])
        else:
            out = "What's this?"
    return out

async def send_marvelous_image(message: discord.Message) -> None:
    today = dt.datetime.now(dt.UTC).weekday()
    is_sunday = today == 6

    image_url = sunday_image_url if is_sunday else weekday_image_url

    await message.channel.send(image_url)

async def handle_keyword_reaction(message: discord.Message) -> None:
    if not isinstance(message.channel, (discord.TextChannel, discord.Thread, discord.ForumChannel)):
        # For DMs or non-guild channels, skip emoji search that requires guild
        return

    content = message.content

    if "marvelous" in content.lower() and not message.author.bot:
        await send_marvelous_image(message)

    keyword = None
    if "GoodMorning" in content:
        keyword = "GoodMorning"
    elif "GoodNight" in content:
        keyword = "GoodNight"
    if not keyword:
        return

    emoji = discord.utils.find(lambda e: e.name == keyword, message.guild.emojis)
    if emoji:
        await message.add_reaction(emoji)
