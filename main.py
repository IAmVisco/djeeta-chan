# djeeta 2.0 (working title)

# importing libraries
import discordbot as discord
import random
import asyncio

bot = discord.DiscordBot()

# list of insults
insults_list = (
	" is a filthy weeb.",
	", you're like Rapunzel but instead of letting down your hair you let everyone down.",
	", you got rejected by Aniki.",
	", is your ass jealous of the amount of shit that just came out of your mouth?",
	", if I wanted to kill myself I'd climb your ego and jump to your IQ.",
	", your family tree must be a cactus because everybody on it is a prick",
	", you're so ugly, when your mom dropped you off at school she got a fine for littering",
	", it's better to let someone think you are an idiot than to open your mouth and prove it",
	", your birth certificate is an apology letter from the condom factory",
	", the only way you'll ever get laid is if you crawl up a chicken's ass and wait",
	", if laughter is the best medicine, your face must be curing the world",
	", it looks like your face caught on fire and someone tried to put it out with a hammer",
	", what language are you speaking? Cause it sounds like bullshit.",
	", I wasn't born with enough middle fingers to let you know how I feel about you.",
	", looking at you, I understand why some animals eat their young.",
	", you are proof that evolution CAN go in reverse.",
	", if I had a face like yours, I'd sue my parents",
	", I'm jealous of all the people that haven't met you.",
	", you're the reason the gene pool needs a lifeguard.",
	", I would love to insult you...but that would be beyond the level of your intelligence.",
	", calling you an idiot would be an insult to all stupid people.",
	", I would ask you how old you are but I know you can't count that high.",
	", Roses are red violets are blue, God made me pretty, what happened to you?",
	", You are so ugly when you looked in the mirror your reflection walked away.",
	", Don't you love nature, despite what it did to you?",
	", Hell is wallpapered with all your deleted selfies.",
	", Shock me, say something intelligent.",
	", Keep talking, someday you'll say something intelligent!",
	", Brains aren't everything. In your case they're nothing.",
	", Karma takes too long, I'd rather beat the shit out of you just now.",
	", Ever since I saw you in your family tree I've wanted to cut it down.",
	", Normal people live and learn. You just live.",
	", You are not as bad as people say, you are much, much worse.",
	", If I had a dollar for every time you said something smart, I'd be broke.",
	", You want an insult? Right, look at the mirror.",
	", Just because you have one doesn't mean you have to act like one.",
	", Aww, it's so cute when you try to talk about things you don't understand.",
	", Did your parents keep the placenta and throw away the baby?",
	", You should need a license to be that ugly.",
	", Are you always this stupid or is today a special occasion?",
	", If what you don't know can't hurt you, you're invulnerable.",
)

# user id of people to be insulted
victim_list = (
	# "some_id_here",
	# "more_id"
)

# variable answers for ~choose command
fancy_answer = (
	"Without a doubt it's ",
	"It's certanly ",
	"I would go for ",
	"Signs point to ",
	"I choose ",
	"Lady luck told me it's "
)

# put bad words here to be filtered in chat
badWords = (
	
)

# dictionary with gifs for ~gif command
gifDict = {
	'dayum': 'https://imgur.com/a/pEJEL',
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
	'shwing': 'https://imgur.com/a/BBr3X',
	'chino': 'https://imgur.com/jxHLO4g',
	'excited': 'https://imgur.com/a/dVAmT',
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

# defining some variables
gm         = True
gn         = True

@bot.event
async def on_member_join(member):
	"""Greets new member on join.
	
	I have no idea how member.server is working, 
	sometimes it does, sometimes it does not.
	"""
	await bot.send_message(member.server, 'Welcome {0.mention} to {1.name}!'.format(member, member.server))

@bot.event
async def on_message(message):
	global gm
	global gn

	# scripted interactions on messages
	if not message.author.bot:
		if gm and "GoodMorning" in message.content and "say" not in message.content.lower():
			await bot.send_message(message.channel, "GoodMorning")
			gm = False
			await asyncio.sleep(60)
			gm = True
		elif gn and "GoodNight" in message.content and "say" not in message.content.lower():
			await bot.send_message(message.channel, "GoodNight")
			gn = False
			await asyncio.sleep(60)
			gn = True
		elif "/o/" in message.content.lower():
			await bot.send_message(message.channel, "\\o\\")
		elif "\\o\\" in message.content.lower():
			await bot.send_message(message.channel, "/o/")
		elif message.content.lower() == "ayy":
			await bot.send_message(message.channel, "lmao")
		elif "\\o/" in message.content.lower():
			await bot.send_message(message.channel, "\\o/")

	# profanity filter, specify bad words in tuple on the beggining
	for word in badWords:
		if word in message.content.lower():
			await bot.delete_message(message)
			await bot.send_message(message.channel, message.author.mention + " is a baka")
			await bot.add_roles(message.author, discord.utils.get(message.server.roles, name = 'mute')) # set role for mute here
			await asyncio.sleep(300)
			await bot.remove_roles(message.author, discord.utils.get(message.server.roles, name = 'mute'))

	# double prefix, in this example works with specified prefix and !
	if message.content.startswith('!'):
		message.content = message.content.replace('!', bot.command_prefix)

	# echo on 3 msges
	logs = []
	async for msg in bot.logs_from(message.channel, limit = 3):
		logs.append(msg)
	if logs[0].content == logs[1].content == logs[2].content and not \
	(logs[0].author.bot or logs[1].author.bot or logs[2].author.bot):
		await bot.send_message(message.channel, logs[0].content)

	await bot.process_commands(message)

if __name__ == "__main__":
    bot.load_cogs()
    bot.run()