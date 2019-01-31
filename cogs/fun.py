import os
import aiohttp
import discord
from datetime import datetime
from discord.ext import commands

from utils import random_color


class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.res_path = os.getcwd() + "/res/"

    @commands.command()
    @commands.guild_only()
    async def emo(self, ctx, emo_name):
        """Shows requested emote.

        List available by typing <prefix>emolist.
        """
        try:
            await ctx.send(file=discord.File(self.res_path + "emotes/" + emo_name.lower() + '.png'))
        except FileNotFoundError:
            await ctx.send("No match found.")

    @commands.command()
    @commands.guild_only()
    async def siete(self, ctx, emo_name):
        """Shows sietefied emote.

        List available by typing <prefix>emolist.
        """
        try:
            await ctx.send(file=discord.File(self.res_path + "siete/" + emo_name.lower() + '.png'))
        except FileNotFoundError:
            await ctx.send("No match found.")

    @commands.command()
    @commands.guild_only()
    async def emolist(self, ctx):
        """Shows all avaible emotes."""
        await ctx.send('<https://imgur.com/a/jmGm3>\nHidden cuz big pic')

    @commands.command()
    @commands.guild_only()
    async def f(self, ctx, *, target=None):
        """Press F to pay respects."""
        if target is None:
            msg = "**" + ctx.author.name + "** has paid their respects."
        else:
            msg = "**" + ctx.author.name + "** has paid their respects for **" + target + ".**"
        embed = discord.Embed(description=msg, color=random_color(), timestamp=datetime.utcnow())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def shrug(self, ctx):
        """Shows shrug emote."""
        await ctx.send("¯\\_(ツ)_/¯")

    @commands.command()
    @commands.guild_only()
    async def lenny(self, ctx):
        """Shows lenny emote."""
        await ctx.send("( ͡° ͜ʖ ͡°)")

    @commands.command()
    @commands.guild_only()
    async def tableflip(self, ctx):
        """Shows tableflip emote."""
        await ctx.send("(╯°□°）╯︵ ┻━┻")

    @commands.command()
    @commands.guild_only()
    async def mai(self, ctx):
        """Equivalent to ~emo mai"""
        await ctx.send(file=discord.File(self.res_path + "emotes/mai.png"))

    @commands.command()
    async def advice(self, ctx):
        """Fetches random advice from adviceslip.com."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.adviceslip.com/advice") as resp:
                result = await resp.json(content_type=None)
        await ctx.send(result.get("slip").get("advice"))

    @commands.command()
    @commands.guild_only()
    async def quote(self, ctx):
        """Fetches random quote from forismatic.com"""
        url = "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                result = await resp.json()
        await ctx.send("{0} - **{1}**".format(result.get("quoteText"), result.get("quoteAuthor")))

    @commands.command()
    @commands.guild_only()
    async def yesno(self, ctx):
        """Sends GIF with yes or no answer."""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://yesno.wtf/api") as resp:
                result = await resp.json()
        await ctx.send(result.get("image"))


def setup(bot):
    bot.add_cog(Fun(bot))
