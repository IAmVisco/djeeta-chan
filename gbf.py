import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone
from utils import RandomColor
import requests

eventsEmbed = discord.Embed(title="Event schedule",
                            description="Schedule for June",
                            color=RandomColor())
events = [
    ["Together in Song", "30/06 - 08/07"],
    ["Rise of the Beasts", "09/07 - 15/07"],
    ["Guild Wars (Earth enemies)", "16/07 - 23/07"],
    ["Poacher's Day (Rerun)", "24/07 - 30/07"],
    ["New Scenario Event", "31/07 - 08/08"]
]

for event in events:
    eventsEmbed.add_field(name=event[0], value=event[1], inline=False)

gw_mode = False
gwstart = datetime(2018, 4, 22, 19, 0, 0, 0, timezone('Asia/Tokyo'))
prelimsend = datetime(2018, 4, 23, 23, 59, 0, 0, timezone('Asia/Tokyo'))


class GBF():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def events(self):
        """Shows upcoming events schedule.

        If it's outdated, bot host forgot to update it.
        Poke him/her with a stick, tenderly.
        """
        await self.bot.say(embed=eventsEmbed)

    @commands.command()
    async def gw(self):
        """Shows GW timings.

        Very broken on certain days, will fix someday.
        """
        if gw_mode:
            if (datetime.now(timezone('Asia/Tokyo')).day == gwstart.day and
                datetime.now(timezone('Asia/Tokyo')).hour >= 19) or \
               datetime.now(timezone('Asia/Tokyo')).day == gwstart.day + 1:
                await self.bot.say(':point_right: :clock12: | Prelims end in ' +
                                   str(prelimsend.day - datetime.now(timezone('Asia/Tokyo')).day) +
                                   ' days ' + str(prelimsend.hour -
                                                  datetime.now(timezone('Asia/Tokyo')).hour) +
                                   ' hours ' + str(prelimsend.minute -
                                                   datetime.now(timezone('Asia/Tokyo')).minute) +
                                   ' minutes.')
            elif (datetime.now(timezone('Asia/Tokyo')).hour >= 7):
                if 23 - datetime.now(timezone('Asia/Tokyo')).hour != 0:
                    await self.bot.say(':point_right: :clock12: | Round ' +
                                       str(datetime.now(timezone('Asia/Tokyo')).day - 25) +
                                       ' ends in ' +
                                       str(23 - datetime.now(timezone('Asia/Tokyo')).hour) +
                                       ' hours ' +
                                       str(60 - datetime.now(timezone('Asia/Tokyo')).minute) +
                                       ' minutes.')
                else:
                    await self.bot.say(':point_right: :clock12: | Round ' +
                                       str(datetime.now(timezone('Asia/Tokyo')).day - 25) +
                                       ' ends in ' +
                                       str(60 - datetime.now(timezone('Asia/Tokyo')).minute) +
                                       ' minutes.')

            elif datetime.now(timezone('Asia/Tokyo')).day - 25 <= 5:  # day of start(14) + 2
                if 6 - datetime.now(timezone('Asia/Tokyo')).hour != 0:
                    await self.bot.say(':point_right: :clock7: | Round ' +
                                       str(datetime.now(timezone('Asia/Tokyo')).day - 25) +
                                       ' starts in ' +
                                       str(6 - datetime.now(timezone('Asia/Tokyo')).hour) +
                                       ' hours ' +
                                       str(60 - datetime.now(timezone('Asia/Tokyo')).minute) +
                                       ' minutes.')
                else:
                    await self.bot.say(':point_right: :clock7: | Round ' +
                                       str(datetime.now(timezone('Asia/Tokyo')).day - 25) +
                                       ' starts in ' +
                                       str(60 - datetime.now(timezone('Asia/Tokyo')).minute) +
                                       ' minutes.')
            else:
                await self.bot.say('Guild Wars 38 is over, thanks for your hard work.')
        else:
            await self.bot.say('Guild Wars 39 will have **Earth** enemies. ' +
                               'It is scheduled to arrive on Jule 16th.')

    @commands.command()
    async def wiki(self, *, query: str):
        """Searches gbf.wiki"""
        url = 'https://gbf.wiki/api.php?action=query&' + \
              'list=search&format=json&utf8=&srsearch=' + query
        r = requests.get(url=url).json()
        if r["query"]["searchinfo"]["totalhits"] != 0:
            await self.bot.say("https://gbf.wiki/" +
                               r['query']['search'][0]["title"].replace(' ', '_'))
        else:
            await self.bot.say("Nothing found, please check your input and try again.")


def setup(bot):
    bot.add_cog(GBF(bot))
