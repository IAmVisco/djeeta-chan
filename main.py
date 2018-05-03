#djeeta 2.0 (working title)

#===To-do list===
#Remake trials/showdowns
#Make ~slam
#Music? Maybe?
#Make DB for multi server ~~drifting~~ settings
#make proper ~help/wait for docu on existing one

#importing libraries
import discordbot as discord
import random
import logging
import asyncio
import os
import requests
import ast
from datetime import datetime
from time import strftime
from pytz import timezone
from PIL import Image, ImageOps
import urllib.request

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


fancy_answer_list = (
	"Without a doubt it's ",
	"It's certanly ",
	"I would go for ",
	"Signs point to ",
	"I choose ",
	"Lady luck told me it's "
)

# badWords = (
# 	# 'nigger',
# 	# 'faggot',
# )

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
# Help me review and add more gifs! https://pastebin.com/v3u8DG22

gw_mode    = False
gwstart    = datetime(2018, 4, 22, 19, 0, 0, 0, timezone('Asia/Tokyo'))
prelimsend = datetime(2018, 4, 23, 23, 59, 0, 0, timezone('Asia/Tokyo'))
startTime  = datetime.now()
gm         = True
gn         = True
casuals_id = '265292778756374529'

#creating events embed
eventsEmbed=discord.Embed(title="Event schedule", description="Schedule for May", color=0x0bbbae)
events = [
	["A Thousand Reasons" , "30/04 - 08/05"],
	["The Girl who Leapt Through Mountains (Rerun)" , "09/05 - 14/05"],
	["Xeno Vohu Clash (Rerun)" , "15/05 - 22/05"],
	["Guild Wars (Water Enemies)", "23/05 - 30/05"],
	["New Scenario Event", "31/05 - 09/06"]
]

for event in events:
	eventsEmbed.add_field(name = event[0], value = event[1], inline = False)

gifEmbed=discord.Embed(title = 'GIF List', description = 'Use ~gif <name> to post a GIF, names are shown below')
for pair in gifDict.items():
	gifEmbed.add_field(name = pair[0], value = pair[1], inline = True)

def strfdelta(tdelta, fmt):
    """ timedelta formatter """
    d = {"D": tdelta.days}
    d["h"], rem = divmod(tdelta.seconds, 3600)
    d["m"], d["s"] = divmod(rem, 60)
    return fmt.format(**d)

#starting up
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	await bot.change_presence(game = discord.Game(name="Djeetablue Fantasy"))

#anti-lurking message
@bot.event
async def on_member_join(member):
	if member.server.id == casuals_id:
		await asyncio.sleep(5)
		await bot.add_roles(member, discord.utils.get(member.server.roles, name = "pubs"))

@bot.command()
async def emo(emoName:str):
	"""Shows requested emote.

	Displays requested emote, list avaible by typing
	<prefix>emolist
	""" 	
	try:
		await bot.upload(os.getcwd() + '/res/emotes/' + emoName.lower() + '.png')
	except:
		await bot.say("No match found.")

@bot.command()
async def siete(emoName:str):	
	"""Shows sietefied emote.

	Displays requested emote, list avaible by typing
	<prefix>emolist
	""" 
	try:
		await bot.upload(os.getcwd() + '/res/siete/' + emoName.lower() + '.png')
	except:
		await bot.say("No match found.")

@bot.command()
async def emolist():
	"""Shows all avaible emotes.

	Sends imgur album link with all 
	avaible emotes and siete emotes.
	"""
	await bot.say('<https://imgur.com/a/jmGm3>\nHidden cuz big pic')

@bot.command()
async def gif(gifName:str):
	"""Shows requested GIF emote.

	Full list of GIF emotes is avaible
	by typing <prefix>giflist
	"""
	try:
		await bot.say(gifDict[gifName.lower()])
	except:
		await bot.say("No match found.")

@bot.command()
async def giflist():
	"""Shows full list of GIF emotes avaible.

	Sends embed with the list of all gif emotes.
	Unlike usual emotes list, this one is 
	auto-generated.
	"""
	await bot.say(embed = gifEmbed)

#ninja echo
@bot.command(pass_context = True, description = 'I will say smth. Make me say smth bad and I will ~~stab you~~ add you to visctoms :dagger:') # description left for memes sake
async def say(ctx, *, msg:str):
	"""Echoes message.

	Will delete and echo passed message
	after 1 second.
	"""
	await bot.delete_message(ctx.message)
	await bot.type()
	await asyncio.sleep(1)
	await bot.say(msg)

@bot.command(pass_context = True)
async def roles(ctx):
	"""Shows roles list.

	Disaplys roles that are lower in role hierarchy
	than bot's role. If this doesn't work, check code
	and bot's role name, case matters.
	"""
	tmp = ":pencil: __**These are the roles I can (un)assign you with:**__"
	if ctx.message.server.id == '267994151436550146':
		bot_role = discord.utils.get(ctx.message.server.roles, name = "Djeeta-chan")
	else:
		bot_role = discord.utils.get(ctx.message.server.roles, name = "Bot")

	# lists the roles the bot can assign
	for role in ctx.message.server.roles:
		if role < bot_role and not role.is_everyone:
			tmp += "\n  - " + role.name
	print(tmp)
	await bot.say(tmp)

@bot.command(pass_context = True)
async def role(ctx, *, role: discord.Role):
	"""Assigns or unassigns the role.

	Same command is used for both assigning and 
	unassigning. Case-sensitive.
	"""
	if ctx.message.server.id != casuals_id:
		try:
			if role in ctx.message.author.roles:
				await bot.remove_roles(ctx.message.author, role)
				await bot.say(ctx.message.author.mention + ", the role " + role.name + " has been removed from your roles.")
			else:	
				await bot.add_roles(ctx.message.author, role)
				await bot.say(ctx.message.author.mention + ", the role " + role.name + " has been added to your roles.")
		except Exception as e:
			await bot.say("Please check your input again. The format is ~role <role name>. Available roles can be viewed using ~roles.")

@bot.command()
async def roll(roll:str):
	"""Will roll a dice for you.

	Rolls a dice both in WoW (/roll N) and 
	in DnD (/roll NdN) formats, where N is either
	range or (number of dices)d(range).
	"""
	out = ":game_die: | Hmm, let it be **"
	try:
		if "d" not in roll:
			out += str(random.randint(1, int(roll)))
		elif roll[0] == "d":
			out += str(random.randint(1, int(roll[1:])))
		else:
			for i in range(int(roll.split("d")[0])):
				out += "\nDice " + str(i+1) + ": " + str(random.randint(1,int(roll.split("d")[1])))
		out += "**"
	except:
		out = "Please check your input again. The format is ~roll <number> or ~roll <NdN>."
	await bot.say(out)

@bot.command(pass_context = True)
async def ping(ctx):
	"""Checks if bot is alive.

	No, it's not ping to game server.
	"""
	msg = await bot.say("Pong!")
	await bot.edit_message(msg, "Pong! Time taken: " + str(int((msg.timestamp - 
		ctx.message.timestamp).microseconds // 1000)) + "ms")

@bot.command(pass_context = True)
async def choose(ctx):
	"""Makes a choice.

	Makes random choice out of all provided variants,
	separated by comma.
	"""
	variants = ctx.message.content[8:]
	if ',' in variants and variants[-1] != ',':
		variants = variants.strip().split(',')
		await bot.say(":thinking:| " + random.choice(fancy_answer_list) + 
			"**" + random.choice(variants).strip() + "!**")
	else:
		await bot.say("Please check your input again. The format is ~choose <Option 1>, <Option 2>, etc.")

@bot.command()
async def events():
	"""Shows upcoming events schedule.

	If it's outdated, bot host forgot to update it.
	Poke him/her with a stick, tenderly.
	"""
	await bot.say(embed = eventsEmbed)

@bot.command(pass_context = True)
async def f(ctx):
	"""Press F to pay respects.

	Pays respect in general or for a specified cause.
	"""
	if ctx.message.content.strip() == "~f":
		respectsMessage = discord.Embed(description = "**" + ctx.message.author.name + 
		"** has paid their respects.\n", color=0x8b75a5) # + str(count) + " total."
	else:
		respectsMessage = discord.Embed(description = "**" + ctx.message.author.name + 
		"** has paid their respects for **" + ctx.message.content[3:] + ".**\n", color=0x8b75a5)# + str(count) + " total."
	await bot.say(embed = respectsMessage)

@bot.command()
async def yesno():
	"""Will send GIF with yes or no answer."""
	await bot.say(requests.get("http://yesno.wtf/api").json()['image'])

@bot.command()
async def zen():
	"""Sends zen quote from GitHub"""
	await bot.say(requests.get("https://api.github.com/zen").text)

@bot.command()
async def gw():
	"""Shows GW timings.

	Very broken on certain days, will fix someday.
	"""
	if gw_mode:
		if (datetime.now(timezone('Asia/Tokyo')).day == gwstart.day and 
			datetime.now(timezone('Asia/Tokyo')).hour >= 19) or \
			datetime.now(timezone('Asia/Tokyo')).day == gwstart.day + 1:
			await bot.say(':point_right: :clock12: | Prelims end in '+ str(prelimsend.day -
				datetime.now(timezone('Asia/Tokyo')).day) + ' days ' + str(prelimsend.hour -
				datetime.now(timezone('Asia/Tokyo')).hour) + ' hours ' + str(prelimsend.minute -
				datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')	
		# elif (datetime.now(timezone('Asia/Tokyo')).day <= gwstart.day):
		# 	if (gwstart.hour - datetime.now(timezone('Asia/Tokyo')).hour >= 0):
		# 		await bot.say(':point_right: :clock1: | Prelims start in '+ str(gwstart.day - 
		# 			datetime.now(timezone('Asia/Tokyo')).day) + ' days ' + str(gwstart.hour - 
		# 			datetime.now(timezone('Asia/Tokyo')).hour) + ' hours ' + str(60 - 
		# 			datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')
		# 	else:
		# 		await bot.say(':point_right: :clock1: | Prelims start in ' + str(24 - 
		# 			(gwstart.hour - datetime.now(timezone('Asia/Tokyo')).hour)) + ' hours ' + str(60 - 
		# 			datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')
		elif (datetime.now(timezone('Asia/Tokyo')).hour >= 7):
			if 23 - datetime.now(timezone('Asia/Tokyo')).hour != 0:
				await bot.say(':point_right: :clock12: | Round ' + 
					str(datetime.now(timezone('Asia/Tokyo')).day - 24) +
					' ends in ' + str(23 - datetime.now(timezone('Asia/Tokyo')).hour) + ' hours ' +
					str(60 - datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')
			else:
				await bot.say(':point_right: :clock12: | Round ' + str(datetime.now(timezone('Asia/Tokyo')).day - 24) + 
					' ends in ' + str(60 - datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')

		elif datetime.now(timezone('Asia/Tokyo')).day - 24 <= 5: # day of start(14) + 2
			if 6 - datetime.now(timezone('Asia/Tokyo')).hour != 0:
				await bot.say(':point_right: :clock7: | Round ' + str(datetime.now(timezone('Asia/Tokyo')).day - 24) + 
					' starts in ' + str(6 - datetime.now(timezone('Asia/Tokyo')).hour) + ' hours ' + 
					str(60 - datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')
			else:
				await bot.say(':point_right: :clock7: | Round ' + str(datetime.now(timezone('Asia/Tokyo')).day - 24) + 
					' starts in ' + str(60 - datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')
		else:
			await bot.say('Guild Wars 37 is over, thanks for your hard work.')
	else:
		await bot.say('Guild Wars 38 will have **Water** enemies. It is scheduled to arrive in May.')

@bot.command(pass_context = True)
async def disgusting(ctx):
	"""Shows random disgusted anime girl.

	You can specify number of pic, no list avaible though.
	Final is a perv.
	"""
	msg = ctx.message.content
	if msg.strip() == "~disgusting":
		await bot.upload(os.getcwd() + '/res/disgusting/' + str(random.randint(1,38)) + '.png')
	elif int(msg[12:]) > 0 and int(msg[12:]) < 39 :
		await bot.upload(os.getcwd() + '/res/disgusting/' + msg[12:] + '.png')

@bot.command(pass_context = True)
async def bigmoji(ctx):
	"""Shows full size of emoji.

	Just send emoji right after command name.
	"""
	try:
		str = ctx.message.content[9:]
		fields = str.split(':')
		mim = '.gif' if fields.pop(0) == "<a" else '.png'
		await bot.say('https://discordapp.com/api/emojis/' 
					+ fields[1][:len(fields[1]) - 1] + mim)
	except:
		await bot.say('Sorry I can\'t retrieve this emote')

@bot.command()
async def mai():
	"""Equivalent to ~emo mai"""
	await bot.upload(os.getcwd() + '/res/emotes/mai.png')

@bot.command()
async def avatar(user: discord.Member):
	"""Shows avatar of the user"""
	await bot.say(user.avatar_url)

@bot.command()
async def wiki(*, query: str):
	"""Searches gbf.wiki"""
	url = 'https://gbf.wiki/api.php?action=query&list=search&format=json&utf8=&srsearch=' + query
	r = requests.get(url = url).json()
	print(query)
	if r["query"]["searchinfo"]["totalhits"] != 0:
		await bot.say("https://gbf.wiki/" + r['query']['search'][0]["title"].replace(' ', '_'))
	else:
		await bot.say("Nothing found, please check your input and try again.")

@bot.command(pass_context = True)
async def userinfo(ctx, user: discord.Member = None):
	"""Shows info about user."""
	if user is None:
		user = ctx.message.author

	userInfo = discord.Embed(title = user.name + '#' + user.discriminator, color = 0x07f7e2)
	userInfo.set_thumbnail(url = user.avatar_url)
	userInfo.add_field(name = 'Status', value = user.status)
	userInfo.add_field(name = 'ID', value = user.id)
	userInfo.add_field(name = 'Account creation date', 
		value = user.created_at.strftime("%d %b %Y %H:%M %Z"))
	userInfo.add_field(name = 'Server join date', 
		value = user.joined_at.strftime("%d %b %Y %H:%M %Z"))
	userInfo.set_footer(text = strfdelta(datetime.now() - startTime, 
		"Alive for {D} days {h} hours {m} minutes {s} seconds."), 
		icon_url = bot.user.avatar_url)
	await bot.say(embed = userInfo)

@bot.command(pass_context = True)
async def serverinfo(ctx):
	"""Shows info about server"""
	server = ctx.message.server;
	serverInfo = discord.Embed(title = server.name, color = 0x07f7e2)
	serverInfo.set_thumbnail(url = server.icon_url)
	serverInfo.add_field(name = 'ID', value = server.id)
	serverInfo.add_field(name = 'Owner', value = server.owner.name + 
		'#' + server.owner.discriminator)
	serverInfo.add_field(name = 'Region', value = server.region)
	serverInfo.add_field(name = 'Members', value = server.member_count)
	serverInfo.add_field(name = 'Channels', value = sum(1 for _ in server.channels))
	serverInfo.add_field(name = 'Creation date', 
		value = server.created_at.strftime("%d %b %Y %H:%M %Z"))
	serverInfo.add_field(name = 'Roles list', 
		value = ', '.join(role.name for role in server.roles))
	serverInfo.set_footer(text = strfdelta(datetime.now() - startTime, 
		"Alive for {D} days {h} hours {m} minutes {s} seconds."), 
		icon_url = bot.user.avatar_url)
	await bot.say(embed = serverInfo)

@bot.command()
async def shrug():
	"""Shows shrug emote, useful if you are on phone."""
	await bot.say("¯\_(ツ)_/¯")

@bot.command()
async def lenny():
	"""Shows lenny emote, useful if you are on phone."""
	await bot.say("( ͡° ͜ʖ ͡°)")

@bot.command()
async def tableflip():
	"""Shows tableflip emote, useful if you are on phone."""
	await bot.say("(╯°□°）╯︵ ┻━┻")

@bot.event 
async def on_member_update(before, after):
	# If Casuals or GuestStar role is added, remove pub role

	cas_role = [before.roles[i] for i in range(len(before.roles)) if str(before.roles[i]) == "Casuals" or before.roles[i].id == "340178120919351307"]
	old_match = len(cas_role)
	cas_role = [after.roles[i] for i in range(len(after.roles)) if str(after.roles[i]) == "Casuals" or after.roles[i].id == "340178120919351307"]
	if len(cas_role) <= old_match:
		return
	pub_role = [before.roles[i] for i in range(len(before.roles)) if before.roles[i].id == "419124938247766026"]
	if len(pub_role) == 0:
		return
	#assured that he still has the pub role since only 1 update at a time, but for ensurace
	pub_role = [after.roles[i] for i in range(len(after.roles)) if after.roles[i].id == "419124938247766026"]
	if len(pub_role) == 0:
		return
	await bot.remove_roles(after, pub_role[0])

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

	# # profanity filter
	# if message.server.id == casuals_id:
	# 	for word in badWords:
	# 		if word in message.content.lower():
	# 			await bot.delete_message(message)
	# 			await bot.send_message(message.channel, message.author.mention + " is a baka")
	# 			await bot.add_roles(message.author, discord.utils.get(message.server.roles, name = 'nadeko-mute'))
	# 			await asyncio.sleep(300)
	# 			await bot.remove_roles(message.author, discord.utils.get(message.server.roles, name = 'nadeko-mute'))

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

bot.run()