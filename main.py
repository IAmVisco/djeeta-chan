#djeeta 2.0 (working title)

#===To-do list===
#Remake trials/showdowns
#Music? Maybe?
#Make DB for multi server ~~drifting~~ settings

#importing libraries
import discordbot as discord
import random
import aiohttp
import asyncio

from pyquery import PyQuery as pq
import json
import datetime
import re
from pathlib import Path

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

def check_files():
	path = Path("res/twitter.json")
	if not path.is_file():
		path.touch()
		path.write_text(
			"{\n"+
				"\t\"config\":{\n"+
					"\t\t\"type\": \"Config\",\n"+
					"\t\t\"interval\": 30,\n"+
					"\t\t\"include\": [ \"GBF\" ]\n"+
				"\t},\n"+
				"\t\"GBF\":{\n"+
					"\t\t\"url\": \"https://twitter.com/granbluefantasy\",\n"+
					"\t\t\"channels\": [ \"396353984287342593\", \"460113527697309696\" ],\n"+
				 	# "\t\t\"interval\": 30,\n"+
					"\t\t\"discriminators\": []\n"+
				"\t}\n"+
			"}")

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

def processTwitter(feed_name, channels, data):
	# _UAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"'
	twitter = "https://twitter.com"
	disc = list()
	hasUpdate = False

	async with aiohttp.ClientSession() as session:
		html = await fetch(session, url)

	d = pq(html)
	tweetList = d("#stream-items-id li[data-item-id]")

	for item in tweetList.items():
		# check if its a retweet
		tweet = item(".tweet")
		permalink = tweet.attr("data-permalink-path")
		if not permalink.startswith("/"+data["url"].split('/')[-1]): #  "/granbluefantasy"):
			# It's a retweet
			continue

		tweet_id = tweet.attr("data-item-id")
		disc.append(tweet_id)
		if tweet_id not in data["discriminators"]:
			hasUpdate = True
		else:
			continue

		screen_name = tweet.attr("data-screen-name")
		user_name = tweet.attr("data-name")

		header = tweet("div.stream-item-header")
		avatar = header("img.avatar").attr("src")
		datetime_ms = int(header("span[data-time-ms]").attr("data-time-ms"))

		textContainer = tweet("div.js-tweet-text-container")
		textContainer("a.u-hidden").remove()

		for a in textContainer("a").items():
			raw = a.html()
			# #hash and @name
			raw = re.sub(r"</?s>(\n)?", "", raw)
			raw = re.sub(r"</?b>(\n)?", "**", raw)
			raw = re.sub(r"</?u>(\n)?", "__", raw)
			hre = a.attr("href")
			if not hre.startswith("http"):
				hre = twitter + hre
			raw = "["+raw+"]("+hre+")"
			a.replace_with(raw)
		description = textContainer.text()

		imgUrls = list()

		if tweet.hasClass("has-cards"):
			imgContainer = tweet("div[data-image-url]")
			for img in imgContainer.items():
				imgUrls.append(img.attr("data-image-url"))
		# Build the embed
		embed = discord.Embed(title = "Link to Tweet",
				description = description,
				timestamp = datetime.datetime(1970,1,1).utcfromtimestamp((datetime_ms/1000)),
				url = twitter+permalink)
		embed.set_author(name = "@"+screen_name, url=data['url'], icon_url=avatar)
		embed.set_thumbnail(url=avatar)

		if len(imgUrls) > 0:
			embed.set_image(url=imgUrls.pop(0))

		for channel in channels:
			await bot.send_message(channel, embed=embed)

		while len(imgUrls) > 0:
			iu = imgUrls.pop(0)
			embed = discord.Embed(title = "Link to Tweet",
				timestamp = datetime.datetime(1970,1,1).utcfromtimestamp((datetime_ms/1000)),
				url = twitter+permalink)
			embed.set_author(name = "@"+screen_name, url=data['url'], icon_url=avatar)
			embed.set_thumbnail(url=avatar)
			embed.set_image(iu)
			for channel in channels:
				await bot.send_message(channel, embed=embed)
	if hasUpdate:
		# save new list
		data["discriminators"] = disc
	return hasUpdate

def rebuildTwitterData(oldData):
	newData = {
		'config': {
			'type': "Config",
			'interval': 30,
			'include': list()
		}
	}

	for o in oldData:
		newData["config"]["include"].append(o)
		newData[o] = {
			'url': oldData[o]['url'],
			'channels': oldData[o]['channels'],
			'discriminators': oldData[o]['discriminators']
		}
	return newData

async def feeder():
	#check feed forever
	# print("Starting Feed.")
	check_files()
	# url = 'https://twitter.com/granbluefantasy'
	_TWITTER_FEED_DATA = {}
	_FEED_CHANNELS = {}

	with open("res/twitter.json","r") as read_file:
		_TWITTER_FEED_DATA = json.load(read_file)


	try:
		print("Twitter Feed " + _TWITTER_FEED_DATA["config"]["type"])
	except Exception as e:
		# Will throw error if config doesnt exist and make a config
		_TWITTER_FEED_DATA = rebuildTwitterData()
		with open("res/twitter.json", "w") as write_file:
			json.dump(_TWITTER_FEED_DATA, write_file, indent=4)


	for feed in _TWITTER_FEED_DATA["config"]["include"]:
		_FEED_CHANNELS[feed] = list()
		for chid in _TWITTER_FEED_DATA[feed]["channels"]:
			_FEED_CHANNELS[feed].append(bot.get_channel(chid))


	while(1):
		hasUpdate = False
		for feed in _TWITTER_FEED_DATA["config"]["include"]:
			hasUpdate = processTwitter(feed, _FEED_CHANNELS[feed], _TWITTER_FEED_DATA[feed]) or hasUpdate

		if hasUpdate:
			# save new list
			# _TWITTER_FEED_DATA[feed_name]["discriminators"] = disc
			with open("res/twitter.json", "w") as write_file:
				json.dump(_TWITTER_FEED_DATA, write_file, indent=4)

		await asyncio.sleep(_TWITTER_FEED_DATA["config"]["interval"])


# def loop_feeds():
# 	feeder()

# def looper(loop):
# 	asyncio.set_event_loop(loop)
# 	loop.run_until_complete(feeder())

@bot.event
async def on_ready():
	print('Logged in as:')
	print('Username: ' + bot.user.name)
	print('ID: ' + bot.user.id)
	print('------')
	await bot.change_presence(game=discord.Game(name='{}help for help'.format(bot.command_prefix)))
	if not hasattr(bot, 'uptime'):
		bot.uptime = datetime.datetime.utcnow()

	try:
		loop = asyncio.get_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(feeder())
	except Exception as e:
		print("Loop already started")

if __name__ == "__main__":
	bot.load_cogs()
	bot.run()