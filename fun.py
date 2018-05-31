import discord
from discord.ext import commands
from utils import RandomColor
import os
import random
import requests
import asyncio

gifDict = {
	'dayum': 'https://imgur.com/a/pEJEL',
	# 'mmm': 'https://imgur.com/gBvDKwc',
	'patpat': 'https://imgur.com/a/XnD3V',
	'fu': 'https://imgur.com/a/2OQZW',
	'salt': 'https://imgur.com/a/K3PLQ',
	'drool': 'https://imgur.com/a/iKOMU',
	'stop': 'https://imgur.com/a/OC7en',
	'steel': 'https://imgur.com/a/hOBRw',
	'welcome': 'https://imgur.com/a/u174P',
	'snek': 'https://imgur.com/a/u174P',
	'rolling': 'https://imgur.com/a/tIpbN',
	'police': 'https://imgur.com/a/aIPPX',
	'hkzoom': 'https://imgur.com/a/OLr8Y',
	'anikiw': 'https://imgur.com/a/hydJh',
	'despair': 'https://imgur.com/a/tIpbN',
	# 'milos': 'https://imgur.com/a/LEXHN',
	'shwing': 'https://imgur.com/a/BBr3X',
	'chino': 'https://imgur.com/jxHLO4g',
	'excited': 'https://imgur.com/a/dVAmT',
	# 'boobs': 'https://imgur.com/a/gu5zO',
	'bless': 'https://imgur.com/qp3hEkk',
	'kagami': 'https://imgur.com/a/5EDPs',
	'execution': 'https://imgur.com/a/TpCOW',
	'joker': 'https://imgur.com/a/bNhnD',
	'trueform': 'https://imgur.com/a/bNhnD',
	'reeee': 'https://imgur.com/a/HnCji',
	'umad': 'https://imgur.com/a/HnCji',
	'spin': 'https://imgur.com/a/N6DTW',
	'smile': 'https://imgur.com/a/s1CJN',
	'umiface': 'https://imgur.com/a/rLURu',
	'nice': 'https://imgur.com/a/mgw6A',
	'laugh': 'https://imgur.com/a/ps5I5'
}
# More gifs https://pastebin.com/v3u8DG22

gifEmbed = discord.Embed(title = 'GIF List', description = 
	'Use ~gif <name> to post a GIF, names are shown below', color = RandomColor())

for pair in gifDict.items():
	gifEmbed.add_field(name = pair[0], value = pair[1], inline = True)

class Fun():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context = True)
	async def disgusting(self, ctx):
		"""Shows random disgusted anime girl.
		
		You can specify number of pic, no list avaible though.
		Final is a perv.
		"""
		msg = ctx.message.content
		if msg.strip() == "~disgusting":
			await self.bot.upload(os.getcwd() + '/res/disgusting/' + str(random.randint(1,38)) + '.png')
		elif int(msg[12:]) > 0 and int(msg[12:]) < 39 :
			await self.bot.upload(os.getcwd() + '/res/disgusting/' + msg[12:] + '.png')

	@commands.command()
	async def emo(self, emoName:str):
		"""Shows requested emote.

		List avaible by typing <prefix>emolist.
		""" 	
		try:
			await self.bot.upload(os.getcwd() + '/res/emotes/' + emoName.lower() + '.png')
		except:
			await self.bot.say("No match found.")

	@commands.command()
	async def siete(self, emoName:str):
		"""Shows sietefied emote.

		List avaible by typing <prefix>emolist.
		""" 
		try:
			await self.bot.upload(os.getcwd() + '/res/siete/' + emoName.lower() + '.png')
		except:
			await self.bot.say("No match found.")

	@commands.command()
	async def emolist(self):
		"""Shows all avaible emotes."""
		await self.bot.say('<https://imgur.com/a/jmGm3>\nHidden cuz big pic')

	@commands.command(pass_context = True)
	async def f(self, ctx):
		"""Press F to pay respects."""
		if ctx.message.content.strip() == "~f":
			respectsMessage = discord.Embed(description = "**" + ctx.message.author.name + 
			"** has paid their respects.\n", color = RandomColor()) # + str(count) + " total."
		else:
			respectsMessage = discord.Embed(description = "**" + ctx.message.author.name + 
			"** has paid their respects for **" + ctx.message.content[3:] + ".**\n", color = RandomColor())# + str(count) + " total."
		await self.bot.say(embed = respectsMessage)

	@commands.command()
	async def gif(self, gifName:str):
		"""Shows requested GIF emote.

		Full list of GIF emotes is avaible
		by typing <prefix>giflist
		"""
		try:
			await self.bot.say(gifDict[gifName.lower()])
		except:
			await self.bot.say("No match found.")

	@commands.command()
	async def giflist(self):
		"""Shows full list of GIF emotes avaible."""
		await self.bot.say(embed = gifEmbed)

	@commands.command()
	async def shrug(self):
		"""Shows shrug emote."""
		await self.bot.say("¯\_(ツ)_/¯")

	@commands.command()
	async def lenny(self):
		"""Shows lenny emote."""
		await self.bot.say("( ͡° ͜ʖ ͡°)")

	@commands.command()
	async def tableflip(self):
		"""Shows tableflip emote."""
		await self.bot.say("(╯°□°）╯︵ ┻━┻")

	@commands.command()
	async def mai(self):
		"""Equivalent to ~emo mai"""
		await self.bot.upload(os.getcwd() + '/res/emotes/mai.png')

	#ninja echo
	@commands.command(pass_context = True, description = 'I will say smth. Make me say smth bad and I will ~~stab you~~ add you to visctoms :dagger:') # description left for memes sake
	async def say(self, ctx, *, msg:str):
		"""Echoes message.

		Will delete and echo passed message
		after 1 second.
		"""
		await self.bot.delete_message(ctx.message)
		await self.bot.type()
		await asyncio.sleep(1)
		await self.bot.say(msg)

	@commands.command()
	async def zen(self):
		"""Sends zen quote from GitHub"""
		await self.bot.say(requests.get("https://api.github.com/zen").text)

	@commands.command(pass_context = True)
	async def poll(self, ctx):
		"""Creates quick poll with reactions on the message."""
		await self.bot.add_reaction(ctx.message, '✅')
		await self.bot.add_reaction(ctx.message, '❎')

def setup(bot):
	bot.add_cog(Fun(bot))