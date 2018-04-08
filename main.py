#djeeta 2.0 (working title)

#===To-do list===
#Remake trials/showdowns
#Make ~slam
#Music? Maybe?
#Make DB for multi server ~~drifting~~ settings
#make proper ~help/wait for docu on existing one

#importing libraries
import discord
from discord.ext import commands
import random
import logging
import asyncio
import os
import requests
import ast
from datetime import datetime, timedelta
from pytz import timezone
from PIL import Image, ImageOps
import urllib.request

#enabling logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename = 'errors.log', encoding = 'utf-8', mode = 'w')
handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# list of insults
insults_list = [
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
]

# user id of people to be insulted
victim_list = [
	# "185069144184455168", # Visco
	# "186873040292806656", # Naddie
	# "155763234899492864", # Sleepy
	# "235080660442677248", # RedTF
	# "174852783084666880", # D.E.D
	# "195463465861644288", # Eu
	# "229273041954144257" # Sun
]

# wrong_names = [
# 	"Anre",
# 	"Tweyen",
# 	"Threo",
# 	"Feower",
# 	"Seox",
# 	"Seofon",
# 	"Eahta",
# 	"Niyon",
# 	"Tien"
# ]

fancy_answer_list = [
	"Without a doubt it's ",
	"It's certanly ",
	"I would go for ",
	"Signs point to ",
	"I choose ",
	"Lady luck told me it's "
]

badWords = [
	'nigger',
	'faggot',
]

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
# on review
# worms https://cdn.discordapp.com/attachments/348218497635188738/418486661249499136/Australien_worms.gif
# buttblow http://1.media.dorkly.cvcdn.com/17/90/e957f68f0285658f03972f32126cbd8e.gif
# you diedhttps://cdn.discordapp.com/attachments/348218497635188738/418484586989879296/IcNRfCv.gif
# spoopy https://cdn.discordapp.com/attachments/348218497635188738/418483087291187200/1517614650820.gif
# yagami https://imgur.com/gallery/PqVNv54
# aizen https://cdn.discordapp.com/attachments/348218497635188738/418489907284017172/1307488195874.gif
# flyer https://cdn.discordapp.com/attachments/348218497635188738/418490600950595585/giant.gif
# swimsuit https://cdn.discordapp.com/attachments/348218497635188738/418491805349183488/1311802255647.gif

# no name
# https://78.media.tumblr.com/a0160ed8bb1b955a25f676da6d33da2f/tumblr_ntcha1rO5A1u0tkulo1_500.gif

gw_mode = False
gwstart    = datetime(2018, 4, 22, 19, 0, 0, 0, timezone('Asia/Tokyo'))
prelimsend = datetime(2018, 4, 23, 23, 59, 0, 0, timezone('Asia/Tokyo'))
gm = True
gn = True

#creating events embed
eventsEmbed=discord.Embed(title="Event schedule", description="Schedule for April", color=0x0bbbae)
events = [
	["Robomi Z" , "31/03 - 08/04"],
	["Detective Conan Collab" , "08/04 - 20/04"],
	["Guild Wars (Dark Enemies)", "22/04 - 29/04"],
	["New Scenario Event", "30/04 - 08/05"]
]

for event in events:
	eventsEmbed.add_field(name=event[0], value=event[1], inline=False)

gifEmbed=discord.Embed(title = 'GIF List', description = 'Use ~gif <name> to post a GIF, names are shown below')
for pair in gifDict.items():
	gifEmbed.add_field(name = pair[0], value = pair[1], inline = True)
	gifEmbed.set_footer(text = 'Help me review and add more gifs! https://pastebin.com/v3u8DG22')

#assigning prefix and description
description = '''Multipurpose GBF oriented bot with useful commands and a bunch of emotes!'''
bot = commands.Bot(command_prefix = '~', description = description)

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
	if member.server.id == '267994151436550146':
		await bot.send_message(member.server, 'Welcome {0.mention} to {1.name}!'.format(member, member.server))
	elif member.server.id == '265292778756374529':
		await asyncio.sleep(5)
		await bot.add_roles(member, discord.utils.get(member.server.roles, name = "pubs"))

#our beloved emotes
@bot.command(description = 'I will show your desired emote!')
async def emo(emoName:str):	
	try:
		await bot.upload(os.getcwd() + '/res/emotes/' + emoName.lower() + '.png')
	except:
		await bot.say("No match found.")

@bot.command(description = 'I will show your desired siete emote!')
async def siete(emoName:str):	
	try:
		await bot.upload(os.getcwd() + '/res/siete/' + emoName.lower() + '.png')
	except:
		await bot.say("No match found.")

@bot.command(description = 'I will show you a list with all emotes!')
async def emolist():
	await bot.say('<https://imgur.com/a/jmGm3>\nHidden cuz big pic')

@bot.command(description = 'I Will show you gif emoji!')
async def gif(gifName:str):
	try:
		await bot.say(gifDict[gifName.lower()])
	except:
		await bot.say("No match found.")

@bot.command(description = 'I will show you a list of animated emojis!')
async def giflist():
	await bot.say(embed = gifEmbed)

#ninja echo
@bot.command(pass_context = True, description = 'I will say smth. Make me say smth bad and I will ~~stab you~~ add you to visctoms :dagger:')
async def say(ctx, *, msg:str):
	await bot.delete_message(ctx.message)
	await bot.type()
	await asyncio.sleep(1)
	await bot.say(msg)

#roles list
@bot.command(pass_context = True, description = 'I will show you a list of roles that can be (un)assigned.')
async def roles(ctx):
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

#assigning and unassigning roles
@bot.command(pass_context = True, description = 'I will (un)assign you desired role!')
async def role(ctx, *, role: discord.Role):
	if ctx.message.server.id != '265292778756374529':
		try:
			if role in ctx.message.author.roles:
				await bot.remove_roles(ctx.message.author, role)
				await bot.say(ctx.message.author.mention + ", the role " + role.name + " has been removed from your roles.")
			else:	
				await bot.add_roles(ctx.message.author, role)
				await bot.say(ctx.message.author.mention + ", the role " + role.name + " has been added to your roles.")
		except Exception as e:
			await bot.say("Please check your input again. The format is ~role <role name>. Available roles can be viewed using ~roles.")

#rollin' rollin'
@bot.command(description = 'I will roll a dice for you!')
async def roll(roll:str):
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

#ping-pong
@bot.command(pass_context = True, description = 'Check if I\'m alive!')
async def ping(ctx):
	msg = await bot.say("Pong!")
	await bot.edit_message(msg, "Pong! Time taken: " + str(int((msg.timestamp - 
		ctx.message.timestamp).microseconds // 1000)) + "ms")

#choose smth
@bot.command(pass_context = True, description = 'I will make a choice for you! \
							The format is ~choose <Option 1>, <Option 2>, etc.')
async def choose(ctx):
	variants = ctx.message.content[8:]
	if ',' in variants:
		variants = variants.strip().split(',')
		await bot.say(":thinking:| " + random.choice(fancy_answer_list) + 
			"**" + random.choice(variants).strip() + "!**")
	else:
		await bot.say("Please check your input again. The format is ~choose <Option 1>, <Option 2>, etc.")


	# old code that i need to remake to avoid crashes with spaces overload
	# if ',' in choices:
	# 	choices = choices.strip().split(',')
	# 	await bot.say(":thinking:| I choose **" + random.choice(choices) + "!**")
	# else:
	# 	await bot.say("Please check your input again. The format is ~choose <Option 1>, <Option 2>, etc.")

#events
@bot.command(description = 'I will show schedule of events from this month!')
async def events():
	await bot.say(embed = eventsEmbed)

#F
@bot.command(pass_context = True, description = 'Press F to pay respects.')
async def f(ctx):
	if ctx.message.content.strip() == "~f":
		respectsMessage = discord.Embed(description = "**" + ctx.message.author.name + 
		"** has paid their respects.\n", color=0x8b75a5) # + str(count) + " total."
	else:
		respectsMessage = discord.Embed(description = "**" + ctx.message.author.name + 
		"** has paid their respects for **" + ctx.message.content[3:] + ".**\n", color=0x8b75a5)# + str(count) + " total."
	await bot.say(embed = respectsMessage)

#yesno
@bot.command(description = 'I will make a decision for you!')
async def yesno():
	await bot.say(requests.get("http://yesno.wtf/api").json()['image'])

#git api test 'n stuffs
@bot.command(description = 'Random zen quote from GitHub.')
async def zen():
	await bot.say(requests.get("https://api.github.com/zen").text)

@bot.command(description = 'I will show when GW round will start/end!')
async def gw():
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
					str(datetime.now(timezone('Asia/Tokyo')).day - 16) +
					' ends in ' + str(23 - datetime.now(timezone('Asia/Tokyo')).hour) + ' hours ' +
					str(60 - datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')
			else:
				await bot.say(':point_right: :clock12: | Round ' + str(datetime.now(timezone('Asia/Tokyo')).day - 16) + 
					' ends in ' + str(60 - datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')

		elif datetime.now(timezone('Asia/Tokyo')).day - 16 <= 5: # day of start(14) + 2
			if 6 - datetime.now(timezone('Asia/Tokyo')).hour != 0:
				await bot.say(':point_right: :clock7: | Round ' + str(datetime.now(timezone('Asia/Tokyo')).day - 16) + 
					' starts in ' + str(6 - datetime.now(timezone('Asia/Tokyo')).hour) + ' hours ' + 
					str(60 - datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')
			else:
				await bot.say(':point_right: :clock7: | Round ' + str(datetime.now(timezone('Asia/Tokyo')).day - 16) + 
					' starts in ' + str(60 - datetime.now(timezone('Asia/Tokyo')).minute) + ' minutes.')
		else:
			await bot.say('Guild Wars 36 is over, thanks for your hard work.')
	else:
		await bot.say('Guild Wars 37 will have **Dark** enemies. It is scheduled to arrive in late April.')

@bot.command(pass_context = True, description = 'Final is a perv')
async def disgusting(ctx):
	msg = ctx.message.content
	if msg.strip() == "~disgusting":
		await bot.upload(os.getcwd() + '/res/disgusting/' + str(random.randint(1,38)) + '.png')
	elif int(msg[12:]) > 0 and int(msg[12:]) < 39 :
		await bot.upload(os.getcwd() + '/res/disgusting/' + msg[12:] + '.png')

@bot.command(pass_context = True, description = 'I will show bigger version of your emoji!')
async def bigmoji(ctx):
	try:
		str = ctx.message.content[9:]
		fields = str.split(':')
		mim = '.gif' if fields.pop(0) == "<a" else '.png'
		await bot.say('https://discordapp.com/api/emojis/' 
					+ fields[1][:len(fields[1])-1] + mim)
	except:
		await bot.say('Sorry I can\'t retrieve this emote')

@bot.command()
async def mai():
	await bot.upload(os.getcwd() + '/res/emotes/mai.png')

@bot.command(description = "I will retrieve avatar URL of user you provided!")
async def avatar(user: discord.Member):
	await bot.say(user.avatar_url)

@bot.command(description = "I will search gbf.wiki for you!")
async def wiki(*, query: str):
	url = 'https://gbf.wiki/api.php?action=query&list=search&format=json&utf8=&srsearch=' + query
	r = requests.get(url = url).json()
	print(query)
	if r["query"]["searchinfo"]["totalhits"] != 0:
		await bot.say("https://gbf.wiki/" + r['query']['search'][0]["title"].replace(' ', '_'))
	else:
		await bot.say("Nothing found, please check your input and try again.")

# emotes for phone mode
@bot.command()
async def shrug():
	await bot.say("¯\_(ツ)_/¯")

@bot.command()
async def lenny():
	await bot.say("( ͡° ͜ʖ ͡°)")

@bot.command()
async def tableflip():	
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

	# profanity filter
	if message.server.id == '265292778756374529':
		for word in badWords:
			if word in message.content.lower():
				await bot.delete_message(message)
				await bot.send_message(message.channel, message.author.mention + " is a baka")
				await bot.add_roles(message.author, discord.utils.get(message.server.roles, name = 'nadeko-mute'))
				await asyncio.sleep(300)
				await bot.remove_roles(message.author, discord.utils.get(message.server.roles, name = 'nadeko-mute'))

	# double prefix
	if message.content.startswith('!') and not (message.content.startswith('!emo') 
		or message.content.startswith('!events')):
		message.content = message.content.replace('!', '~')

	# echo on 3 msges
	if message.server.id != '265292778756374529':
		logs = []
		async for msg in bot.logs_from(message.channel, limit = 3):
			logs.append(msg)
		if logs[0].content == logs[1].content == logs[2].content and not \
		(logs[0].author.bot or logs[1].author.bot or logs[2].author.bot):
			await bot.send_message(message.channel, logs[0].content)

	await bot.process_commands(message)

#run token
bot.run('Mzg2NDQ5MDkzMzg1Mzg4MDUz.DQQErQ.3SJ8ftYbFWIfQc2lIDVga2cU0cg')

# FOR FUTURE USE
###############################################

# @bot.command()
# async def avatar(user: discord.Member):
# 	await bot.say(user.avatar_url)

# @bot.command()
# async def names(user : discord.User):
# 	await bot.say("Name " + user.name + " Nickname " + user.display_name)

# # bless
# @bot.command()
# async def bless(user: discord.User):
# 	try:
# 		url = urllib.request.Request(user.avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
# 		with urllib.request.urlopen(url) as response, open(os.getcwd() + '/res/etc/image.png', 'wb') as out_file:
# 			data = response.read()
# 			out_file.write(data)
# 		size = 96, 96
# 		mask = Image.open(os.getcwd() + '/res/etc/mask.png').convert("L")
# 		im = Image.open(os.getcwd() + '/res/etc/image.png')
# 		out = ImageOps.fit(im, mask.size, centering = (0.5, 0.5))
# 		out.putalpha(mask)
# 		out.thumbnail(size, Image.ANTIALIAS)
# 		img_w, img_h = out.size
# 		bg = Image.open(os.getcwd() + '/res/etc/bless.png').convert("RGBA")
# 		offset = (160 - img_w // 2, 110 - img_h // 2)
# 		bg.alpha_composite(out, offset)
# 		bg.save(os.getcwd() + '/res/etc/bless_out.png')
# 		await bot.upload(os.getcwd() + '/res/etc/bless_out.png')
# 		os.remove(os.getcwd() + '/res/etc/bless_out.png')
# 		os.remove(os.getcwd() + '/res/etc/image.png')
# 	except:
# 		await bot.say("Check your input and try again. The format is ~bless <mention>")


# DEAD CODE REGION 
###############################################
# trials based on excel table
# @bot.command(description = 'I will show you current or future trial!')
# async def trials():#arg:str):
# 	# if arg == "today":
# 	# 	await bot.say(str(datetime.now(timezone('Europe/Samara')).strftime("%d of %b (today) - ")) + str(sheet.row[datetime.now(timezone('Europe/Samara')).day-1][0]) + " Trial")
# 	# elif arg.isdigit():
# 	# 	await bot.say(arg + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[int(arg)-1][0]) + " Trial")
# 	# elif arg.isalpha():    
# 	# 	for record in range(datetime.now(timezone('Europe/Samara')).day, len(sheet.column[1])):
# 	# 		if arg.lower() == sheet.row[int(record)][0].lower():
# 	# 			await bot.say(str(record+1) + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[record][0]) + " Trial")
# 	# 			break
# 	# else:
# 	# 	await bot.say("Please check your input and try again. Use ~help for more info.")
# 	await bot.say("I'm too lazy to write good code for this one.")
# #showdowns too
# @bot.command(description = 'I will show you current or future showdown!')

# #revealing true self
# @bot.command(pass_context = True, description = 'I will use my powers to reveal true self of the chosen one!')
# async def reveal(ctx, *, userName):
# 	if userName[1] == "@":
# 		user = discord.utils.get(ctx.message.server.members, mention = userName)
# 	else:
# 		user = discord.utils.get(ctx.message.server.members, display_name = userName)
# 	await bot.say("I'm sure it's **" + user.name + "**!")

# async def showdowns():#arg:str):
# 	# if arg == "today":
# 	# 	await bot.say(str(datetime.now(timezone('Europe/Samara')).strftime("%d of %b (today) - ")) + str(sheet.row[datetime.now(timezone('Europe/Samara')).day-1][1]) + " Showdown")
# 	# elif arg.isdigit():
# 	# 	await bot.say(arg + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[int(arg)-1][1]) + " Showdown")
# 	# elif arg.isalpha():    
# 	# 	for record in range(datetime.now(timezone('Europe/Samara')).day, len(sheet.column[1])):
# 	# 		if arg.lower() == sheet.row[int(record)][1].lower():
# 	# 			await bot.say(str(record+1) + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[record][1]) + " showdown")
# 	# 			break
# 	# else:
# 	# 	await bot.say("Please check your input and try again. Use ~help for more info.")
# 	await bot.say("I'm too lazy to write good code for this one.") 

# @bot.event
# async def on_message(message):
# 	await bot.process_commands(message)	

# (message.author.id == 185069144184455168) and 
# pepeGun = discord.utils.get(message.server.emojis, name = 'pepeGun')
# if not pepeGun == None:
# 	for wrong_name in wrong_names:
# 		if wrong_name.lower() in message.content.lower():
# 			await bot.send_message(message.channel, "It's time to stop " + str(pepeGun) +"\nhttps://thumbs.gfycat.com/AdmirableShadyCur-size_restricted.gif")
# 			break

#insults
# if message.author.id in victim_list:
# 	if (message.server.id != "301829994567434241"):
# 		pool = ["🇱", "🇪", "🇼", "🇩", "🍆"]
# 		pool = ["🇸","🇹","🇺","🇵","🇮","🇩"]
# 		if message.author.id in victim_list and random.randint(1,100) == 1:
# 			for letter in pool:
# 				await bot.add_reaction(message, letter)
# 		if (random.randint(1,100) == 1):
# 			await bot.send_message(message.channel, message.author.mention + random.choice(insults_list))

# Beaver is ded MingLow
# if beaver <= 0 and "beaver" in message.content.lower() and ("dead" in message.content.lower() or "ded" in message.content.lower()):
# 	await bot.send_message(message.channel, "MingLow")
# 	beaver = 10