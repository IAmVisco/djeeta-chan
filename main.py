import asyncio
import os
import sys
import traceback
from typing import Any

import discord
import logging
from discord.ext import commands
from utils import process_message_replies, handle_keyword_reaction

__version__: str = '3.2.0'
intents: discord.Intents = discord.Intents.all()
logging.basicConfig(format="%(levelname)s:%(asctime)s:%(message)s", level=logging.INFO, stream=sys.stdout)
bot: commands.Bot = commands.Bot(command_prefix="~",
                   description="Djeeta bot! Has some cool commands and a bunch of emotes.",
                   intents=intents
                   )


@bot.event
async def on_ready() -> None:
    await bot.change_presence(activity=discord.Game(name="~help to help"))
    logging.info(" {0.user.name} bot {1} - Ready. Running on Python v{2.major}.{2.minor}.{2.micro}-{2.releaselevel} "
                 .format(bot, __version__, sys.version_info).center(70, "="))


@bot.event
@commands.guild_only()
async def on_message(message: discord.Message) -> None:
    await handle_keyword_reaction(message)

    out = process_message_replies(message) if not message.author.bot else None

    logs = [message async for message in message.channel.history(limit=3)]
    if logs[0].content == logs[1].content == logs[2].content and not any([msg.author.bot for msg in logs]):
        out = logs[0].content

    if out:
        await message.channel.send(out)

    await bot.process_commands(message)


@bot.event
async def on_command_completion(ctx: commands.Context) -> None:
    if isinstance(ctx.channel, discord.DMChannel):
        template = "{0.author} invoked '{0.message.content}' in {0.channel}"
    else:
        template = "{0.author} invoked '{0.message.content}' in #{0.channel} ({0.guild})"
    logging.info(template.format(ctx))


@bot.event
async def on_command_error(ctx: commands.Context, exception: Exception) -> None:
    if hasattr(ctx.command, 'on_error'):
        return

    cog = ctx.cog
    if cog and commands.Cog._get_overridden_method(cog.cog_command_error) is not None:
        return

    if isinstance(exception, commands.NoPrivateMessage):
        await ctx.send(":warning: | You can't you this command in DMs!")
        return

    if isinstance(exception, commands.errors.MissingRequiredArgument):
        await ctx.send(":warning: | Missing mandatory command arguments!")
        return

    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)


async def main() -> None:
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            await bot.load_extension(f"cogs.{name}")

    async with bot:
        await bot.start(os.environ.get("BOT_TOKEN"))

asyncio.run(main())

