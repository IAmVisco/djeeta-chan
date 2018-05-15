#djeeta 2.0 (working title)

#===To-do list===
#Remake trials/showdowns
#Music? Maybe?
#Make DB for multi server ~~drifting~~ settings

#importing libraries
import discordbot as discord
import random
import asyncio

bot = discord.DiscordBot()

# list of insults
# insults_list = (
# 	" is a filthy weeb.",
# 	", you're like Rapunzel but instead of letting down your hair you let everyone down.",
# 	", you got rejected by Aniki.",
# 	", is your ass jealous of the amount of shit that just came out of your mouth?",
# 	", if I wanted to kill myself I'd climb your ego and jump to your IQ.",
# 	", your family tree must be a cactus because everybody on it is a prick",
# 	", you're so ugly, when your mom dropped you off at school she got a fine for littering",
# 	", it's better to let someone think you are an idiot than to open your mouth and prove it",
# 	", your birth certificate is an apology letter from the condom factory",
# 	", the only way you'll ever get laid is if you crawl up a chicken's ass and wait",
# 	", if laughter is the best medicine, your face must be curing the world",
# 	", it looks like your face caught on fire and someone tried to put it out with a hammer",
# 	", what language are you speaking? Cause it sounds like bullshit.",
# 	", I wasn't born with enough middle fingers to let you know how I feel about you.",
# 	", looking at you, I understand why some animals eat their young.",
# 	", you are proof that evolution CAN go in reverse.",
# 	", if I had a face like yours, I'd sue my parents",
# 	", I'm jealous of all the people that haven't met you.",
# 	", you're the reason the gene pool needs a lifeguard.",
# 	", I would love to insult you...but that would be beyond the level of your intelligence.",
# 	", calling you an idiot would be an insult to all stupid people.",
# 	", I would ask you how old you are but I know you can't count that high.",
# 	", Roses are red violets are blue, God made me pretty, what happened to you?",
# 	", You are so ugly when you looked in the mirror your reflection walked away.",
# 	", Don't you love nature, despite what it did to you?",
# 	", Hell is wallpapered with all your deleted selfies.",
# 	", Shock me, say something intelligent.",
# 	", Keep talking, someday you'll say something intelligent!",
# 	", Brains aren't everything. In your case they're nothing.",
# 	", Karma takes too long, I'd rather beat the shit out of you just now.",
# 	", Ever since I saw you in your family tree I've wanted to cut it down.",
# 	", Normal people live and learn. You just live.",
# 	", You are not as bad as people say, you are much, much worse.",
# 	", If I had a dollar for every time you said something smart, I'd be broke.",
# 	", You want an insult? Right, look at the mirror.",
# 	", Just because you have one doesn't mean you have to act like one.",
# 	", Aww, it's so cute when you try to talk about things you don't understand.",
# 	", Did your parents keep the placenta and throw away the baby?",
# 	", You should need a license to be that ugly.",
# 	", Are you always this stupid or is today a special occasion?",
# 	", If what you don't know can't hurt you, you're invulnerable.",
# )

# user id of people to be insulted
# victim_list = (

# )

# badWords = (
# 	# 'nigger',
# 	# 'faggot',
# )

gm         = True
gn         = True
casuals_id = '265292778756374529'

# # Starting up
# @bot.event
# async def on_ready():
# 	print('Logged in as')
# 	print(bot.user.name)
# 	print(bot.user.id)
# 	print('------')
# 	await bot.change_presence(game = discord.Game(name="Djeetablue Fantasy"))

# @bot.event
# async def on_member_join(member):

@bot.event
async def on_message(message):
	global gm
	global gn

	# random replies
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

	# double prefix
	if message.content.startswith('!') and not (message.content.startswith('!emo') 
		or message.content.startswith('!events')):
		message.content = message.content.replace('!', '~')

	# echo on 3 msges
	if message.server.id != casuals_id:
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