#djeeta 2.0 (working title)
#importing libraries
import discord
from discord.ext import commands
import random
import logging
import asyncio
import os
import requests
import ast
from datetime import datetime
import pyexcel as pe
from pytz import timezone

#enabling logging
logging.basicConfig(level = logging.INFO)

#assigning excel sheet
sheet = pe.get_sheet(file_name = "trials.xlsx")

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
	"185069144184455168", # Visco
	"186873040292806656", # Naddie
	"155763234899492864", # Sleepy
	# "235080660442677248", # RedTF
	# "174852783084666880", # D.E.D
	"195463465861644288" # Eu
]

#creating events embed
eventsEmbed=discord.Embed(title="Event schedule", description="Schedule for July", color=0x0bbbae)
eventsEmbed.add_field(name="Ranger Sign Bravo!", value="30/06 - 08/07", inline=False)
eventsEmbed.add_field(name="Cerberus/Fenrir Showdowns", value="09/07 - 14/07", inline=False)
eventsEmbed.add_field(name="Xeno Vohu Rerun", value="18/07 - 24/07", inline=False)
eventsEmbed.add_field(name="Rise of the Beasts", value="25/07 - 30/07", inline=False)
eventsEmbed.add_field(name="New scenario event", value="31/07 - ???", inline=False)

#assigning prefix and description
description = '''Bot description goes there but idk where it will be shown, 
so I just put some text there. Eu is a hentai baka!'''
bot = commands.Bot(command_prefix = '~', description = description)

#starting up
@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------')
	await bot.change_presence(game = discord.Game(name="Djeetablue Fantasy", url="game.granbluefantasy.jp", type = 1))

#anti-lurking message
@bot.event
async def on_member_join(member):
	await bot.send_message(member.server, 'Welcome {0.mention} to {1.name}!'.format(member, member.server))

#our beloved emotes
@bot.command()
async def emo(emoName:str):	
	try:
		await bot.upload(os.getcwd() + '/res/emotes/' + emoName + '.png')
	except:
		await bot.say("No match found.")

#ninja echo
@bot.command(pass_context = True)
async def say(ctx, msg:str):
	await bot.delete_message(ctx.message)
	await bot.type()
	await asyncio.sleep(1)
	await bot.say(msg)

#context test
@bot.command(pass_context = True)
async def test(ctx):
	await bot.say("Message by " + ctx.message.author.name)

#roles list
@bot.command(pass_context = True)
async def roles(ctx):
	tmp = ":pencil: __**These are the roles I can (un)assign you with:**__"
	bot_role = discord.utils.get(ctx.message.server.roles, name = "Djeeta-chan")

	# lists the roles the bot can assign
	for role in ctx.message.server.roles[1:]:
		if role < bot_role:
			tmp += "\n  - " + role.name

	await bot.say(tmp)	
#assigning and unassigning roles
@bot.command(pass_context = True)
async def role(ctx, *, role: discord.Role):
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
@bot.command()
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
@bot.command(pass_context = True)
async def ping(ctx):
	msg = await bot.say("Pong!")
	await bot.edit_message(msg, "Pong! Time taken: " + str(int((msg.timestamp - ctx.message.timestamp).microseconds//1000)) + "ms")

#choose smth
@bot.command()
async def choose(*choices:str):
    await bot.say(":thinking:| I choose **" + random.choice(choices) + "!**")

#events
@bot.command()
async def events():
	await bot.say(embed = eventsEmbed)

#revealing true self
@bot.command(pass_context = True)
async def reveal(ctx, *, userName):
	if userName[1] == "@":
		user = discord.utils.get(ctx.message.server.members, mention = userName)
	else:
		user = discord.utils.get(ctx.message.server.members, display_name = userName)
	await bot.say("I'm sure it's **" + user.name + "**!")

#trials based on excel table
@bot.command()
async def trials(arg:str):
	if arg == "today":
		await bot.say(str(datetime.now(timezone('Europe/Samara')).strftime("%d of %b (today) - ")) + str(sheet.row[datetime.now(timezone('Europe/Samara')).day-1][0]) + " Trial")
	elif arg.isdigit():
		await bot.say(arg + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[int(arg)-1][0]) + " Trial")
	elif arg.isalpha():    
		for record in range(datetime.now(timezone('Europe/Samara')).day, len(sheet.column[1])):
			if arg.lower() == sheet.row[int(record)][0].lower():
				await bot.say(str(record+1) + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[record][0]) + " Trial")
				break
	else:
		await bot.say("Please check your input and try again. Use ~help for more info.")

#showdowns too
@bot.command()
async def showdowns(arg:str):
	if arg == "today":
		await bot.say(str(datetime.now(timezone('Europe/Samara')).strftime("%d of %b (today) - ")) + str(sheet.row[datetime.now(timezone('Europe/Samara')).day-1][1]) + " Showdown")
	elif arg.isdigit():
		await bot.say(arg + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[int(arg)-1][1]) + " Showdown")
	elif arg.isalpha():    
		for record in range(datetime.now(timezone('Europe/Samara')).day, len(sheet.column[1])):
			if arg.lower() == sheet.row[int(record)][1].lower():
				await bot.say(str(record+1) + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[record][1]) + " showdown")
				break
	else:
		await bot.say("Please check your input and try again. Use ~help for more info.")

#F
@bot.command(pass_context = True)
async def f(ctx):
	with open('respects.txt','r+') as f:
		count = int(f.read()) + 1
		f.seek(0)
		f.truncate()
		f.write(str(count))
	if ctx.message.content.strip() == "~f":
		respectsMessage = discord.Embed(description = "**" + ctx.message.author.name + "** has paid their respects.\n" + str(count) + " total.", color=0x8b75a5)
	else:
		respectsMessage = discord.Embed(description = "**" + ctx.message.author.name + "** has paid their respects for **" + ctx.message.content[3:] + ".**\n" + str(count) + " total.", color=0x8b75a5)
	await bot.say(embed = respectsMessage)

#yesno
@bot.command()
async def yesno():
	await bot.say(ast.literal_eval(requests.get("http://yesno.wtf/api").text.replace("false", "\"false\"")).get('image'))

#insults
@bot.event
async def on_message(message):
	if message.author.id in victim_list:
		if random.randint(1,100) == 1:
			await bot.send_message(message.channel, message.author.mention + random.choice(insults_list))
	await bot.process_commands(message)
	
#run token
bot.run('MzE0Nzk4NjM1NDI0Njc3ODg4.C_9r5w.jgercQMOJwhkkXX01gpFP0VCO2Y')