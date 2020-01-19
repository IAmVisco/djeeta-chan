import os
import psutil
import random
import asyncio
import aiohttp
import discord
import logging
from discord.ext import commands
from collections import Counter
from datetime import datetime

from utils import random_color, get_utc_string, connect_to_db

fancy_answers = (
    "Without a doubt it's",
    "It's certainly",
    "I would go for",
    "Signs point to",
    "I choose",
    "Lady luck told me it's"
)


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self.emoji_url = "https://cdn.discordapp.com/emojis/"

    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Shows avatar of the user."""
        if user is None:
            user = ctx.author
        await ctx.send(user.avatar_url)

    @commands.command()
    async def bigmoji(self, ctx, emoji=None):
        """Shows full size of emoji."""
        if emoji is not None:
            try:
                fields = emoji.split(":")
                mim = ".gif" if fields.pop(0) == "<a" else ".png"
                await ctx.send(self.emoji_url + fields[-1][:-1] + mim)
            except:
                await ctx.send("Sorry, I can't process that.")
        else:
            await ctx.send("You didn't pass an emoji!")

    @commands.command()
    async def calc(self, ctx, *, expr: str):
        """Calculates passed expression.

        Expression you pass will be evaluated by Python
        interpreter with few exceptions so use its syntax if possible.
        """
        try:
            out = ":1234: | Answer is **"
            out += str(eval(expr.replace("^", "**").replace("x", "*").replace(",", "."), {'__builtins__': {}})) + "**."
        except (ValueError, SyntaxError, TypeError):
            out = "Failed to evaluate the expression. Please try again."
        await ctx.send(out)

    @commands.command()
    async def choose(self, ctx, *, variants):
        """Makes a choice.

        The format is <prefix>choose <Option 1>, <Option 2>, etc."""
        if "," in variants:
            options = variants.split(",")
            await ctx.send(":thinking:| {0} **{1}!**".format(random.choice(fancy_answers),
                                                             random.choice(options).strip()))
        else:
            await ctx.send("Please check your input again. The format is ~choose <Option 1>, <Option 2>, etc.")

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        """Shows info about user."""
        if user is None:
            user = ctx.author
        user_info = discord.Embed(title=str(user), color=random_color(), timestamp=datetime.utcnow())
        user_info.set_thumbnail(url=user.avatar_url)
        user_info.add_field(name="Status", value=user.status)
        user_info.add_field(name="ID", value=user.id)
        user_info.add_field(name="Account creation date", value=get_utc_string(user.created_at))
        user_info.add_field(name="Server join date", value=get_utc_string(user.joined_at))
        await ctx.send(embed=user_info)

    @commands.command(aliases=["guildinfo"])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """Shows info about server"""
        guild = ctx.guild
        server_info = discord.Embed(title="{0} (ID: {1})".format(guild.name, guild.id),
                                    color=random_color(),
                                    timestamp=datetime.utcnow())
        server_info.set_thumbnail(url=guild.icon_url)
        server_info.add_field(name="Owner", value=guild.owner)
        server_info.add_field(name="Region", value=guild.region)
        server_info.add_field(name="Members", value=guild.member_count)
        server_info.add_field(name="Roles", value=sum(1 for _ in guild.roles))
        server_info.add_field(name="Channels", value=sum(1 for _ in guild.channels))
        server_info.add_field(name="Creation date", value=get_utc_string(guild.created_at))
        roles_list = ", ".join(role.name for role in guild.roles[::-1])
        if len(roles_list) <= 1024:
            server_info.add_field(name="Roles list", value=roles_list)
        await ctx.send(embed=server_info)

    @commands.command(aliases=["about"])
    async def info(self, ctx):
        """Shows info about bot and bot's developer."""
        info = await self.bot.application_info()
        owner = info.owner
        text_channels, voice_channels = 0, 0
        for channel in self.bot.get_all_channels():
            if isinstance(channel, discord.TextChannel):
                text_channels += 1
            if isinstance(channel, discord.VoiceChannel):
                voice_channels += 1
        memory_usage = self.process.memory_full_info().uss / 1024 ** 2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()

        bot_info = discord.Embed(title="GitHub Repository",
                                 url="https://github.com/IAmVisco/djeeta-chan",
                                 color=random_color(),
                                 timestamp=datetime.utcnow())
        bot_info.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        bot_info.set_thumbnail(url=self.bot.user.avatar_url)
        bot_info.add_field(name="Servers connected", value=len(list(self.bot.guilds)))
        bot_info.add_field(name="Users known", value=len(list(self.bot.get_all_members())))
        bot_info.add_field(name="Channels known", value=f"{text_channels} text/{voice_channels} voice")
        bot_info.add_field(name="Owner", value=owner)
        bot_info.add_field(name="Memory", value=f"{memory_usage:.2f} MiB")
        bot_info.add_field(name="CPU", value=f"{cpu_usage:.2f}% CPU")
        bot_info.set_footer(text="Made with discord.py", icon_url="http://i.imgur.com/5BFecvA.png")
        await ctx.send(embed=bot_info)

    @commands.command()
    async def ping(self, ctx):
        """Checks if bot is alive."""
        msg = await ctx.send("Pong!")
        ping = (msg.created_at - ctx.message.created_at).microseconds // 1000
        await msg.edit(content=f"Pong! Time taken {ping}ms")

    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        """Shows roles list.

        Displays roles that are lower in role hierarchy
        than bot's top role that has 'Manage Roles' permission
        and thus can be managed by bot.
        """
        roles = ctx.guild.me.roles[::-1]
        top_role = next((r for r in roles if r.permissions.manage_roles or r.permissions.administrator), None)
        out = "Seems like I can't manage any roles right now."

        if top_role is not None:
            out = ":pencil: __**These are the roles I can (un)assign you with:**__"
            roles = ctx.guild.roles[::-1]
            for role in roles[:-1]:
                if role < top_role:
                    out += "\n  - " + role.name
        await ctx.send(out)

    @staticmethod
    async def can_process_role(ctx, role):
        if role is None:
            await ctx.send("Please check your input. Roles are case-sensitive, full list available via ~roles.")
            return False

        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send("Sorry but I can't manage roles on this server.")
            return False

        return True

    @staticmethod
    async def add_role(ctx, role):
        await ctx.author.add_roles(role)
        await ctx.send(ctx.author.mention + ", the role " + role.name + " has been added to your roles.")

    @staticmethod
    async def remove_role(ctx, role):
        await ctx.author.remove_roles(role)
        await ctx.send(ctx.author.mention + ", the role " + role.name + " has been removed from your roles.")

    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, *, role: discord.Role = None):
        """Assigns or remove the role. Case-sensitive.

        Same command is used for both assigning and
        unassigned.
        """
        if not await self.can_process_role(ctx, role):
            return

        try:
            if role in ctx.author.roles:
                await self.remove_role(ctx, role)
            else:
                await self.add_role(ctx, role)
        except discord.Forbidden:
            await ctx.send("Sorry, the role is higher in server hierarchy than my own.")

    @commands.command()
    @commands.guild_only()
    async def addrole(self, ctx, *, role: discord.Role = None):
        """Assigns a role. Case-sensitive.

        More explicit way to add a role. Check ~roles
        for the full list."""
        if not await self.can_process_role(ctx, role):
            return

        try:
            if role not in ctx.author.roles:
                await self.add_role(ctx, role)
            else:
                await ctx.send(ctx.author.mention + ", you have that role already!")
        except discord.Forbidden:
            await ctx.send("Sorry, the role is higher in server hierarchy than my own.")

    @commands.command()
    @commands.guild_only()
    async def removerole(self, ctx, *, role: discord.Role = None):
        """Removes a role. Case-sensitive.

        More explicit way to remove a role. Check ~roles
        for the full list."""
        if not await self.can_process_role(ctx, role):
            return

        try:
            if role in ctx.author.roles:
                await self.remove_role(ctx, role)
            else:
                await ctx.send(ctx.author.mention + ", you don't have that role!")
        except discord.Forbidden:
            await ctx.send("Sorry, the role is higher in server hierarchy than my own.")

    @commands.command(aliases=["dice"])
    async def roll(self, ctx, *, roll: str):
        """Will roll a dice for you.

        Rolls a dice in DnD (~roll NdN + N + ...) format.
        To roll [1-N], type ~roll dN.
        """
        header = ":game_die: | Hmm, let it be "
        if "d" in roll:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://rolz.org/api/?" + roll.replace(" ", "") + ".json") as resp:
                    result = await resp.json()
                    number = str(result.get("result"))
                    details = result.get("details").replace(" ", "").replace("+", " + ")
                    details = "" if "+" not in details else details
                    out = f"{header}**{number} {details}**"
        else:
            out = "Please check your input again. The format is ~roll <dN> or ~roll <NdN>."
        await ctx.send(out)

    @commands.command(aliases=["vote"])
    @commands.guild_only()
    async def poll(self, ctx):
        """Creates quick poll with reactions on the message."""
        await ctx.message.add_reaction("✅")
        await ctx.message.add_reaction("❎")

    @commands.command(description="I will say smth. Make me say smth bad and I will ~~stab you~~ add you to visctoms "
                                  ":dagger:")  # description left for memes sake
    @commands.guild_only()
    async def say(self, ctx, *, msg):
        """Echoes message.

        Will delete and echo passed message
        after 1 second.
        """
        await ctx.message.delete()
        await ctx.trigger_typing()
        await asyncio.sleep(1)
        await ctx.send(msg)

    @commands.command()
    async def wiki(self, ctx, *, query: str):
        """Searches gbf.wiki"""
        url = "https://gbf.wiki/api.php?action=query&list=search&format=json&utf8=&srsearch=" + query
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                r = await response.json()
                if r.get("query").get("searchinfo").get("totalhits") != 0:
                    await ctx.send("https://gbf.wiki/" + r.get("query").get("search")[0]["title"].replace(" ", "_"))
                else:
                    await ctx.send("Nothing found, please check your input and try again.")

    @commands.group(invoke_without_command=True, aliases=["gfl"])
    async def gf(self, ctx, nick=None):
        """Shows a list with Girls' Frontline Nicks and UIDs"""
        conn = await connect_to_db()
        if nick is None:
            user_info = discord.Embed(title="Girls' Frontline players list",
                                      color=random_color(),
                                      timestamp=datetime.utcnow())
            res = await conn.fetch("SELECT * FROM gfl ORDER BY uid")
            for record in res:
                user_info.add_field(name=record[1], value=record[2])
            await ctx.send(embed=user_info)
        else:
            user_info = discord.Embed(title="Girls' Frontline user info",
                                      color=random_color(),
                                      timestamp=datetime.utcnow())
            record = await conn.fetchrow(f"SELECT * FROM gfl WHERE LOWER(name)=LOWER('{nick}')")
            user_info.add_field(name=record[1], value=record[2])
            await ctx.send(embed=user_info)
        await conn.close()

    @gf.command(name="add", hidden=True)
    @commands.is_owner()
    async def add_gf_user_to_list(self, ctx, nick: str, uid: int):
        conn = await connect_to_db()
        await conn.execute("INSERT INTO gfl (name, uid) VALUES ($1, $2)", nick, uid)
        await ctx.send(f"Nick {nick} successfully added to the list.")
        await conn.close()

    @commands.group(invoke_without_command=True)
    async def ak(self, ctx, nick=None):
        """Shows a list with Arknights game nicks"""
        conn = await connect_to_db()
        if nick is None:
            user_info = discord.Embed(title="Arknights players list",
                                      color=random_color(),
                                      timestamp=datetime.utcnow())
            res = await conn.fetch("SELECT * FROM arknights ORDER BY name")
            for record in res:
                user_info.add_field(name=record[1], value=record[2])
            await ctx.send(embed=user_info)
        else:
            user_info = discord.Embed(title="Arknights user info",
                                      color=random_color(),
                                      timestamp=datetime.utcnow())
            record = await conn.fetchrow(f"SELECT * FROM arknights WHERE LOWER(name)=LOWER('{nick}')")
            user_info.add_field(name=record[1], value=record[2])
            await ctx.send(embed=user_info)
        await conn.close()

    @ak.command(name="add", hidden=True)
    @commands.is_owner()
    async def add_ak_user_to_list(self, ctx, nick: str, ign: str):
        conn = await connect_to_db()
        await conn.execute("INSERT INTO arknights (name, ign) VALUES ($1, $2)", nick, ign)
        await ctx.send(f"IGN {nick} successfully added to the list.")
        await conn.close()

    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def stats(self, ctx):
        parse_msg = await ctx.send(':arrows_counterclockwise: | **Parsing channels...**')
        c = Counter()
        for ch in ctx.guild.text_channels:
            if ch.permissions_for(ctx.guild.me).read_message_history:
                msges = await ch.history(limit=None).flatten()
                print(f'Received logs for #{ch}')
                for msg in msges:
                    c[msg.author] += 1
                print(f'Done with #{ch}')
            else:
                print(f'Skipping #{ch}')
        print('Parsed everything')
        print(c)
        out = ':chart_with_downwards_trend: | **Top 20 message senders**\n'
        for index, (author, msg_count) in enumerate(c.most_common()[:20], start=1):
            if index == 1:
                medal = ':first_place:'
            elif index == 2:
                medal = ':second_place:'
            elif index == 3:
                medal = ':third_place:'
            else:
                medal = None

            out += f'{index}. {author} - {msg_count}\n' if medal is None else f'{medal} **{author} - {msg_count}**\n'
        await parse_msg.edit(content=out)

    @commands.command(hidden=True)
    async def restart(self, ctx):
        url = os.environ.get("DYNO_URL")
        token = os.environ.get("API_TOKEN")
        headers = {
            "Accept": "application/vnd.heroku+json;version=3",
            "Authorization": f"Bearer {token}"
        }
        await ctx.send(":arrows_counterclockwise: | Restarting...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers):
                    pass
        except aiohttp.ClientError as e:
            logging.error(e)
            await ctx.send(":cold_sweat: | Restart failed, check logs")


def setup(bot):
    bot.add_cog(Utility(bot))
