import os
import re
import random
import aiohttp
import discord
from discord.ext import commands
from datetime import datetime

from utils import random_color

SSR_pool = ("Altair", "Percival", "Charlotta (Water)", "Aglovale", "Izmir", "Siegfried", "Aletheia", "Lancelot (Water)",
            "Yuisis", "Jeanne d'Arc", "Ferry", "Albert", "Seruel", "Baotorda", "Jeanne d'Arc", "Beatrix", "Vira",
            "Vaseraga (Dark)", "Lancelot (Wind)", "Chat Noir", "Catherine", "Petra", "Agielba", "Rosamia", "Vania",
            "Veight", "Zeta (Dark)", "Lancelot and Vane", "Heles", "Nezahualpilli", "Athena", "Anne", "Razia",
            "Arulumaya", "Carmelina", "Azazel", "Forte", "Zeta (Fire)", "Yuel (Fire)", "Tsubasa", "Aoidos", "Vane",
            "Nemone", "Vaseraga (Earth)", "Melissabelle", "Gawain", "Charlotta (Light)", "Silva (Water)", "Lady Grey",
            "Wulf and Renie", "Hallessena", "Melleau", "Anthuria", "Magisa", "Zahlhamelina", "Lily", "Romeo",
            "Cagliostro", "De La Fille", "De La Fille", "Yurius", "Korwa", "Juliet", "Sarunan", "Cagliostro",
            "Marquiares", "Sarunan", "Yngwie", "Silva (Light)", "Cucouroux", "Eustace (Earth)", "Lennah", "Tiamat",
            "Robomi", "Zooey", "Freezie", "Eustace (Dark)", "Societte (Fire)", "Ghandagoza", "Grea", "Aliza",
            "Lady Katapillar and Vira", "Societte (Water)", "Ayer", "Soriz", "Scathacha", "Dorothy and Claudia",
            "Cerberus", "Lunalu", "Metera", "Ilsa", "Metera", "Feena", "Levin Sisters", "Clarisse", "Lilele", "Sophia",
            "Yggdrasil", "Sara", "Arriet", "Selfira", "Clarisse", "Therese", "Yuel (Water)", "Narmaya", "Amira",
            "Yodarha", "Nicholas", "Agni", "Athena", "Michael", "Prometheus", "Satyr", "Sethlans", "Shiva",
            "Sylph, Flutterspirit of Purity", "Twin Elements", "Zaoshen", "Bonito", "Ca Ong", "Europa", "Gabriel",
            "Grani", "Kaguya", "Macula Marius", "Neptune", "Oceanus", "Poseidon, the Tide Father", "Snow White",
            "Varuna", "Ankusha", "Baal", "Cybele", "Gilgamesh", "Godsworn Alexiel", "Gorilla", "Medusa", "Tezcatlipoca",
            "Titan", "Uriel", "Anat, for Love and War", "Freyr", "Garuda", "Garula, Shining Hawk", "Grimnir", "Hamsa",
            "Morrigna", "Nezha", "Quetzalcoatl", "Raphael", "Rose Queen", "Setekh", "Siren", "Zephyrus", "Adramelech",
            "Aphrodite", "Apollo", "Grand Order", "Halluel and Malluel", "Hector", "Lucifer", "Odin", "Thor",
            "Vortex Dragon", "Zeus", "Anubis", "Bahamut", "Dark Angel Olivia", "Hades", "Lich", "Nacht", "Satan",
            "Tsukuyomi", "Typhon")

query = """query ($name: String, $type: MediaType) {
    Media (search: $name, type: $type) {
        title {
            romaji
        }
        description
        siteUrl
        coverImage {
            large
        }
        averageScore
        episodes
        format
        status
        volumes
    }
}"""


class Weeb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.res_path = os.getcwd() + "/res/"

    @commands.command()
    @commands.guild_only()
    async def disgusting(self, ctx, *args):
        """Shows random disgusted anime girl.

        You can specify number of pic, no list available though.
        Final is a perv.
        """
        pic_path = self.res_path + "disgusting/"
        pics = os.listdir(pic_path)
        if args and int(args[0]) <= len(pics):
            await ctx.send(file=discord.File(pic_path + ctx.args[2] + ".png"))
        else:
            await ctx.send(file=discord.File(pic_path + random.choice(pics)))

    @staticmethod
    def _roll_gacha(rolls_count, only_ssr):
        rolls = []
        got_ssr = True
        out = ":game_die: | **You got these items:**\n"
        for i in range(rolls_count):
            x = random.randint(1, 100)
            if x > 97:
                rolls.append("**SSR - {}**".format(random.choice(SSR_pool)))
                got_ssr = False
            elif (i % 9 == 0 or 82 < x < 97) and not only_ssr:
                rolls.append("SR")
            elif not only_ssr:
                rolls.append("R")
        out += ", ".join(rolls)
        if got_ssr:
            out += "\nBetter luck next time!"
        return out

    @commands.command()
    @commands.guild_only()
    async def gacha(self, ctx):
        """Rolls 10 part GBF gacha.

        Rates are adjusted according to
        the game, without any rate ups.
        """
        await ctx.send(self._roll_gacha(10, False))

    @commands.command()
    @commands.guild_only()
    async def spark(self, ctx, *, target=None):
        """Sparks GBF gacha.

        Rates are adjusted according to
        the game, without any rate ups.
        """
        spark = self._roll_gacha(300, True)
        ssr_count = spark.count("SSR")
        ssr_chance = round(ssr_count / 300 * 100, 2)
        if target and any(target.title() in item for item in SSR_pool):
            target = target.title()
        else:
            target = random.choice(SSR_pool)
        spark += f"\nYou got **{ssr_count} SSRs**, your SSR chance was **{ssr_chance}%!**" \
            f"\nYou sparked... **{target}!**"
        await ctx.send(spark)

    @staticmethod
    def get_weeb_embed(data):
        score = str(data.get("averageScore") / 10) + " / 10" if data.get("averageScore") else "Not yet"
        embed = discord.Embed(title=data.get("title").get("romaji"),
                              colour=random_color(), url=data.get("siteUrl"),
                              description=re.sub(r"<.*?>", "", data.get("description")),
                              timestamp=datetime.utcnow())
        embed.set_thumbnail(url=data.get("coverImage").get("large"))
        embed.set_author(name="AniList entry", url="https://anilist.co",
                         icon_url="https://i.imgur.com/TKvkZmo.png")
        embed.add_field(name="Format", value=data.get("format").replace("_", " "))
        embed.add_field(name="Status", value=data.get("status").title().replace("_", " "))
        if data.get("episodes"):
            embed.add_field(name="Episodes", value=data.get("episodes"))
        else:
            embed.add_field(name="Volumes", value=data.get("volumes"))
        embed.add_field(name="Score", value=score)
        return embed

    @staticmethod
    async def get_anilist_data(name, media_type):
        url = "https://graphql.anilist.co"
        payload = {
            "query": query,
            "variables": {
                "name": name,
                "type": media_type
            }
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                res = await response.json()
        return res.get("data").get("Media")

    @staticmethod
    async def send_weeb_info_reply(ctx, media):
        if not media:
            return await ctx.send("Nothing found. Check your input and try again.")
        await ctx.send(embed=Weeb.get_weeb_embed(media))

    @commands.command()
    async def anime(self, ctx, *, name):
        """Fetches anime entry from AniList.

        Because MAL has closed their API. Don't use MAL."""
        media = await self.get_anilist_data(name, "ANIME")
        await self.send_weeb_info_reply(ctx, media)

    @commands.command(aliases=["ln", "novel"])
    async def manga(self, ctx, *, name):
        """Fetches manga/novel entry from AniList.

        Because MAL has closed their API. Don't use MAL."""
        media = await self.get_anilist_data(name, "MANGA")
        await self.send_weeb_info_reply(ctx, media)


def setup(bot):
    bot.add_cog(Weeb(bot))
