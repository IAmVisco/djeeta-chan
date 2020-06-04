import os
import typing
import aiohttp
import discord
from random import randint
from datetime import datetime
from discord.ext import commands
from utils import random_color, get_json_data, connect_to_db


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.res_path = os.getcwd() + "/res/"
        self.ffz_url = "https://api.frankerfacez.com/v1/"

    @commands.command()
    @commands.guild_only()
    async def emo(self, ctx, emo_name):
        """Shows requested emote.

        List available by typing <prefix>emolist.
        """
        try:
            await ctx.send(file=discord.File(self.res_path + "emotes/" + emo_name.lower() + ".png"))
        except FileNotFoundError:
            await ctx.send("No match found.")

    @commands.command()
    @commands.guild_only()
    async def siete(self, ctx, emo_name):
        """Shows sietefied emote.

        List available by typing <prefix>emolist.
        """
        try:
            await ctx.send(file=discord.File(self.res_path + "siete/" + emo_name.lower() + ".png"))
        except FileNotFoundError:
            await ctx.send("No match found.")

    @commands.command()
    @commands.guild_only()
    async def emolist(self, ctx):
        """Shows all avaible emotes."""
        await ctx.send("<https://imgur.com/a/jmGm3>\nHidden cuz big pic")

    @commands.command()
    @commands.guild_only()
    async def ffz(self, ctx, emoticon_name: typing.Optional[str]):
        """Fetches passed emote from FrankerFacesZ."""
        if emoticon_name is None:
            await ctx.send("Please specify emoticon name!")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.ffz_url}emoticons?q={emoticon_name}&sort=count-desc") as resp:
                result = await resp.json(content_type=None)
                emoticons = result.get("emoticons")
                if len(emoticons) == 0:
                    await ctx.send("Nothing was found!")
                    return
                emo = emoticons[0]
                url = None
                emote_size = 4
                while emote_size > 0:
                    url = emo["urls"].get(str(emote_size))
                    if url:
                        break
                    emote_size -= 1
                if url:
                    await ctx.send(f"https:{url}")
                else:
                    await ctx.send("No suitable emoticon link found.")

    @commands.command()
    @commands.guild_only()
    async def f(self, ctx, *, target=None):
        """Press F to pay respects."""
        conn = await connect_to_db()
        respects_amount = await conn.fetchval("""
            UPDATE respects
            SET total = total + 1
            RETURNING total
        """)
        print(respects_amount)
        if target is None:
            msg = "**" + ctx.author.name + "** has paid their respects."
        else:
            msg = "**" + ctx.author.name + "** has paid their respects for **" + target + ".**"
        embed = discord.Embed(description=msg, color=random_color(), timestamp=datetime.utcnow())
        embed.set_footer(text=f"Total: {respects_amount}")
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
        url = "https://api.adviceslip.com/advice"
        result = await get_json_data(url, content_type=None)
        await ctx.send(result.get("slip").get("advice"))

    @commands.command()
    @commands.guild_only()
    async def quote(self, ctx):
        """Fetches random quote from forismatic.com"""
        url = "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
        result = await get_json_data(url)
        await ctx.send("{0} - **{1}**".format(result.get("quoteText").strip(), result.get("quoteAuthor")))

    @commands.command()
    @commands.guild_only()
    async def yesno(self, ctx):
        """Sends GIF with yes or no answer."""
        url = "http://yesno.wtf/api"
        result = await get_json_data(url)
        await ctx.send(result.get("image"))

    @commands.command()
    async def peko(self, ctx, times=None):
        """Sends a lot of pekos."""
        if times and times.isdecimal():
            out = "PE :arrow_upper_right: KO :arrow_lower_right: " * int(times)
        else:
            out = "PE :arrow_upper_right: KO :arrow_lower_right: " * randint(3, 10)
        await ctx.send(out)

    @commands.command(aliases=["emoji"])
    async def nitro(self, ctx, emoji_name, mode=""):
        """Posts an emoji with provided name if it exists on any server the bot is on.

        If optional 'mode' argument is equal to 'huge', will post a link with emoji instead.
        """
        def flatten(list_):
            return list(sum(list_, ()))

        if not emoji_name:
            await ctx.send(":warning: | You have to provide emoji name!")
            return

        try:
            guild_emojis = flatten(map(lambda guild: guild.emojis, self.bot.guilds))
            emoji = next(emoji for emoji in guild_emojis if emoji.name.lower() == emoji_name.lower())
        except StopIteration:
            await ctx.send(":mag: | Didn't find anything with that name!")
            return

        if not emoji.available:
            await ctx.send(":x: | Can't send that :(")
            return

        await ctx.send(emoji if not mode == "huge" else emoji.url)


def setup(bot):
    bot.add_cog(Fun(bot))
