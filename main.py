import discord
import asyncio
import logging
import os
import time
from random import randint
from cleverwrap import CleverWrap

logging.basicConfig(level=logging.INFO)

client = discord.Client()
cw = CleverWrap("CC2giUNPmorTJdrJNPnp2IIND_Q")
start = 0
end = 0

# list of insults
insults_list = [
	" is a filthy weeb.",
	", you're like Rapunzel but instead of letting down your hair you let everyone down.",
	", you got rejected by Aniki.",
	", two wrongs don't make a right. Take your parents for example.",
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


]
# user id of people to be insulted
victim_list = [
	"185069144184455168", # Visco
	"186873040292806656", #Naddie
	# "235080660442677248", # RedTF
	# "174852783084666880", # D.E.D
]

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	djeetablue = discord.Game(name="Djeetablue Fantasy", url="game.granbluefantasy.jp")
	await client.change_presence(game=djeetablue)

@client.event
async def on_member_join(member):
	server = member.server
	fmt = 'Welcome {0.mention} to {1.name}!'
	await client.send_message(server, fmt.format(member, server))

@client.event
async def on_message(message):
	djeeta = client.user
	if message.content.startswith('~emo'):
		try:
			await client.send_file(message.channel, os.getcwd() + '/res/emotes/' + message.content.lstrip('~emo').strip() + '.png')
		except:
			await client.send_message(message.channel, "No match found.")

	elif message.content.startswith("~say ") and message.author.bot == False:
		await client.send_typing(message.channel)
		await asyncio.sleep(1)
		await client.send_message(message.channel, message.content[5:])

	elif message.content == "~roles":
		tmp = ":pencil: __**These are the roles I can (un)assign you with:**__"
		bot_role = discord.utils.get(message.server.roles, name = "Djeeta-chan")

		# lists the roles the bot can assign
		for role in message.server.roles[1:]:
			if role < bot_role:
				tmp += "\n  - " + role.name

		await client.send_message(message.channel, tmp)

	elif message.content.startswith("~role "):
		try:
			role = discord.utils.get(message.server.roles, name = message.content[6:])

			if role in message.author.roles:
				await client.remove_roles(message.author, role)
				await client.send_message(message.channel, message.author.mention + ", the role " + role.name + " has been removed from your roles.")
			else:
				await client.add_roles(message.author, role)
				await client.send_message(message.channel, message.author.mention + ", the role " + role.name + " has been added to your roles.")
		except Exception as e:
			await client.send_message(message.channel, "Please check your input again. The format is ~role <role name>. Available roles can be viewed using ~roles.")

	elif message.content == "~help":
		msg = """
:notepad_spiral:**Here are the list of commands:**
__**~say <words>**__
	*Makes me say something. Try making me say something bad and I'll add you to the victims.:dagger:*
__**~emo <keyword>**__
	*Basically Vampy rip-off. I'm even using the same words and pics. Cheatsheet: https://risend.github.io/vampy/*
__**~roles**__
	*Lists the available roles that can be (un)assigned.*
__**~role <role name>**__
	*Add or remove role from yourself. It'll add if you don't have it and it'll remove if you already have it.*
__**~avatar <@user>**__
	*I will show you user's avatar in full resolution.*
__**~roll <number>**__
	*I will ask RNGesus for random number in range from 1 to number that you should type.*
__**@Djeeta**__
	*Talk to me!*
__**~ping**__
	*Check if I'm alive.*
__**~help**__
	**OMG WHAT DOES THIS COMMAND DO???**

*P.S. My real function is to insult Visco. There's always a 1 percent chance of me throwing an insult.*
*P.S.S. While Visco is my current Master, my real father is Eurea, who decided to stay in the shadows, like ninja, but I want world to know the truth. We will not forget you.*
"""
		await client.send_message(message.channel, msg)
	
	elif message.content == "~daily":
		await client.send_message(message.channel, "**:atm:  |  " + message.author.name + ", you received your :yen: 200 'daily' credits!**")
	elif message.content.startswith("~money "):
		await client.send_message(message.channel, "**:atm:  |  " + message.author.name + ", you received :yen: " + message.content[7:] + " credits!**")

		await client.send_message(message.channel, tmp)

	elif message.content.startswith("~avatar "):
		user = discord.utils.get(message.server.members, mention = message.content[8:])
		await client.send_message(message.channel, user.avatar_url)

	elif message.content.startswith("~roll "):
		roll = message.content[6:]
		out = ":game_die: | Hmm, let it be **"
		try:
			if "d" not in roll:
				out += str(randint(1, int(roll)))
			elif roll[0] == "d":
				out += str(randint(1, int(roll[1:])))
			else:
				for i in range(int(roll.split("d")[0])):
					out += "\nDice " + str(i+1) + ": " + str(randint(1,int(roll.split("d")[1])))
			out += "**"
		except:
			out = "Please check your input again. The format is ~roll <number> or ~roll <NdN>."
		await client.send_message(message.channel, out)

	elif message.content.startswith(djeeta.mention):
		global start
		global end
		if start:
			if end - start > 180:
				cw.reset()
		else:
			start = time.time()
		await client.send_typing(message.channel)
		await asyncio.sleep(1)
		await client.send_message(message.channel, cw.say(message.content[len(djeeta.name)+1:]))
		end = time.time()

	elif message.content == "~ping":
		#global start
		await client.send_message(message.channel, "Pong!")# Time taken - " + str((time.time() - start)) + "ms")
	
	#elif message.content == "~honors":

	if message.author.id in victim_list:
		if randint(1,100) == 1:
			await client.send_message(message.channel, message.author.mention + insults_list[randint(0,len(insults_list) - 1)])


# bot account token
client.run('MzE0Nzk4NjM1NDI0Njc3ODg4.C_9r5w.jgercQMOJwhkkXX01gpFP0VCO2Y')

# for inviting to server
# https://discordapp.com/api/oauth2/authorize?client_id=314798635424677888&scope=bot&permissions=0

# didn't implement because not really useful
# elif message.content == "~hierarchy":
	# tmp = ""
	# tmp_roles = message.server.roles[1:]
	# tmp_roles.sort()
	# tmp_roles = tmp_roles[::-1]
	# for msg in tmp_roles:
	# 	tmp += "\n" + msg.name