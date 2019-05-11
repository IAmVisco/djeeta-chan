import os
import re
import sys
import asyncio
import discord
import logging
import random as r
from discord.ext import commands
from twitter_listener import setup_twitter


logging.basicConfig(format="%(levelname)s:%(asctime)s:%(message)s", level=logging.INFO, stream=sys.stdout)
logging.info("Starting up...")
bot = commands.Bot(command_prefix="~", description="Djeeta bot! Has some cool commands and a bunch of emotes.")

gm_ready, gn_ready = True, True


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="~help to help"))
    setup_twitter(bot)
    logging.info("Ready")


def process_message_replies(message):
    global gm_ready
    global gn_ready
    out = None
    if gm_ready and "GoodMorning" in message.content:
        out = "GoodMorning"
        gm_ready = False
    elif gn_ready and "GoodNight" in message.content:
        out = "GoodNight"
        gn_ready = False
    elif "/o/" in message.content.lower():
        out = "\\o\\"
    elif "\\o\\" in message.content.lower():
        out = "/o/"
    elif re.search(r"(^|\W)(ay{2,})($|\W)", message.content.lower()) is not None:
        out = "LMAO" if "AYY" in message.content else "lmao"
    elif "\\o/" in message.content.lower():
        out = "\\o/"
    elif re.search(r"(^|\W)(owo)($|\W)", message.content.lower()) is not None:
        if r.randint(1, 100) <= 20:
            out = r.choice(["kys", "uwu", "o3o", " *nuzzles wuzzles*", "no", "Rawr xD", "·///·"])
        else:
            out = "What's this?"

    return out


@bot.event
@commands.guild_only()
async def on_message(message):
    global gm_ready
    global gn_ready

    out = process_message_replies(message) if not message.author.bot else None

    logs = await message.channel.history(limit=3).flatten()
    if logs[0].content == logs[1].content == logs[2].content and not any([msg.author.bot for msg in logs]):
        out = logs[0].content

    if out:
        await message.channel.send(out)

    await bot.process_commands(message)

    if not any([gm_ready, gn_ready]):
        await asyncio.sleep(60)
        gm_ready = gn_ready = True


@bot.event
async def on_command_completion(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        template = "{0.author} invoked '{0.message.content}' in {0.channel}"
    else:
        template = "{0.author} invoked '{0.message.content}' in #{0.channel} ({0.guild})"
    logging.info(template.format(ctx))


# @bot.event  # TODO: properly override this
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.NoPrivateMessage):
#         await ctx.send("You can't you this command in DMs!")


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

bot.run(os.environ.get("BOT_TOKEN"))
