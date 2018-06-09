import discord
from discord.ext import commands
from discordbot.bot_utils import checks, config
from time import strftime
from utils import RandomColor, strfdelta
from datetime import datetime
import requests
import random
import psycopg2

fancy_answers = (
	"Without a doubt it's ",
	"It's certanly ",
	"I would go for ",
	"Signs point to ",
	"I choose ",
	"Lady luck told me it's "
)

casuals_id = '265292778756374529'

config = config.Config('settings.json', directory="")
conn = psycopg2.connect(config.get("DB_URL", ""), sslmode = 'require')
db = conn.cursor()

class Utility():
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context = True)
	async def avatar(self, ctx, user: discord.Member=None):
		"""Shows avatar of the user"""
		if user is None:
			user = ctx.message.author
		await self.bot.say(user.avatar_url)

	@commands.command(pass_context = True)
	async def bigmoji(self, ctx):
		"""Shows full size of emoji."""
		try:
			str = ctx.message.content[9:]
			fields = str.split(':')
			mim = '.gif' if fields.pop(0) == "<a" else '.png'
			await self.bot.say('https://discordapp.com/api/emojis/' 
						+ fields[1][:len(fields[1]) - 1] + mim)
		except:
			await self.bot.say('Sorry I can\'t retrieve this emote')

	@commands.command()
	async def calc(self, *, expr: str):
		"""Calculates passed expression.

		Expression you pass will be evaluated by Python
		compiler with few exceptions so use its syntax if possible.
		"""
		try:
			out = ":1234: | Answer is **"
			out += str(eval(expr.replace("^", "**").replace("x", "*")))#, {'__builtins__':{}})) + "**."
		except:
			out = "Failed to evaluate the expression. Please try again."
		await self.bot.say(out)

	@commands.command(pass_context = True)
	async def choose(self, ctx):
		"""Makes a choice."""
		variants = ctx.message.content[8:]
		if ',' in variants and variants[-1] != ',':
			variants = variants.strip().split(',')
			await self.bot.say(":thinking:| " + random.choice(fancy_answers) + 
				"**" + random.choice(variants).strip() + "!**")
		else:
			await self.bot.say("Please check your input again. The format is ~choose <Option 1>, <Option 2>, etc.")

	@commands.command(pass_context = True)
	async def userinfo(self, ctx, user: discord.Member = None):
		"""Shows info about user."""
		if user is None:
			user = ctx.message.author
		userInfo = discord.Embed(title = str(user), color = RandomColor())
		userInfo.set_thumbnail(url = user.avatar_url)
		userInfo.add_field(name = 'Status', value = user.status)
		userInfo.add_field(name = 'ID', value = user.id)
		userInfo.add_field(name = 'Account creation date', 
			value = user.created_at.strftime("%d %b %Y %H:%M %Z"))
		userInfo.add_field(name = 'Server join date', 
			value = user.joined_at.strftime("%d %b %Y %H:%M %Z"))
		userInfo.set_footer(text = strfdelta(datetime.utcnow() - self.bot.uptime, 
			"Alive for {D} days {h} hours {m} minutes {s} seconds."), 
			icon_url = self.bot.user.avatar_url)
		await self.bot.say(embed = userInfo)

	@commands.command(pass_context = True)
	async def serverinfo(self, ctx):
		"""Shows info about server"""
		server = ctx.message.server;
		serverInfo = discord.Embed(title = 
			server.name + ' (ID: ' + server.id + ')', color = RandomColor())
		serverInfo.set_thumbnail(url = server.icon_url)
		serverInfo.add_field(name = 'Owner', value = server.owner)
		serverInfo.add_field(name = 'Region', value = server.region)
		serverInfo.add_field(name = 'Members', value = server.member_count)
		serverInfo.add_field(name = 'Roles', value = sum(1 for _ in server.roles))
		serverInfo.add_field(name = 'Channels', value = sum(1 for _ in server.channels))
		serverInfo.add_field(name = 'Creation date', 
			value = server.created_at.strftime("%d %b %Y %H:%M %Z"))
		rolesList = ', '.join(role.name for role in server.role_hierarchy)
		if len(rolesList) < 1025:
			serverInfo.add_field(name = 'Roles list', value = rolesList)
		serverInfo.set_footer(text = strfdelta(datetime.utcnow() - self.bot.uptime, 
			"Alive for {D} days {h} hours {m} minutes {s} seconds."), 
			icon_url = self.bot.user.avatar_url)
		await self.bot.say(embed = serverInfo)

	@commands.command()
	async def botinfo(self):
		"""Shows info about bot and bot's developer."""
		owner = await self.bot.get_user_info(self.bot.config.get("meta", {}).get("owner", ""))
		botInfo = discord.Embed(title = 'GitHub Repository', 
			url = 'https://github.com/IAmVisco/djeeta-chan', color = RandomColor())
		botInfo.set_author(name = str(self.bot.user) + ' ID :' + self.bot.user.id)
		botInfo.set_thumbnail(url = self.bot.user.avatar_url)
		botInfo.add_field(name = 'Servers connected', value = sum(1 for _ in self.bot.servers))
		botInfo.add_field(name = 'Users known', value = sum(1 for _ in self.bot.get_all_members()))
		botInfo.add_field(name = 'Channels known', value = sum(1 for _ in self.bot.get_all_channels()))
		botInfo.add_field(name = 'Owner', value = owner)
		botInfo.set_footer(text = strfdelta(datetime.utcnow() - self.bot.uptime, 
			"Alive for {D} days {h} hours {m} minutes {s} seconds."), 
			icon_url = self.bot.user.avatar_url)
		await self.bot.say(embed = botInfo)

	@commands.command(pass_context = True)
	async def ping(self, ctx):
		"""Checks if bot is alive.

		No, it's not ping to game server.
		"""
		msg = await self.bot.say("Pong!")
		await self.bot.edit_message(msg, "Pong! Time taken: " + str(int((msg.timestamp - 
			ctx.message.timestamp).microseconds // 1000)) + "ms")

	@commands.command(pass_context = True)
	async def roles(self, ctx):
		"""Shows roles list.

		Disaplys roles that are lower in role hierarchy
		than bot's role. If this doesn't work, check code
		and bot's role name, case matters.
		"""
		tmp = ":pencil: __**These are the roles I can (un)assign you with:**__"
		bot_role = discord.utils.get(ctx.message.server.roles, name = "Djeeta")
		if bot_role is None:
			bot_role = discord.utils.get(ctx.message.server.roles, name = "Bot")

		# lists the roles the bot can assign
		for role in ctx.message.server.roles:
			if role < bot_role and not role.is_everyone:
				tmp += "\n  - " + role.name
		await self.bot.say(tmp)

	@commands.command(pass_context = True)
	async def role(self, ctx, *, role: discord.Role):
		"""Assigns or unassigns the role.

		Same command is used for both assigning and 
		unassigning. Case-sensitive.
		"""
		print(role)
		if ctx.message.server.id != casuals_id:
			if role is not None:
				if role in ctx.message.author.roles:
					await self.bot.remove_roles(ctx.message.author, role)
					await self.bot.say(ctx.message.author.mention + ", the role " + 
						role.name + " has been removed from your roles.")
				else:	
					await self.bot.add_roles(ctx.message.author, role)
					await self.bot.say(ctx.message.author.mention + ", the role " + 
						role.name + " has been added to your roles.")
			else:
				await self.bot.say("Please check your input again. Roles are case-sensitive, available roles can be viewed using ~roles.")

	@commands.command()
	async def roll(self, roll: str):
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
		await self.bot.say(out)

	@commands.command()
	async def yesno(self):
		"""Sends GIF with yes or no answer."""
		await self.bot.say(requests.get("http://yesno.wtf/api").json()['image'])

	@commands.group(invoke_without_command = True)
	async def gf(self, nick=None):
		"""Shows a list with Girls' Frontline Nicks and UIDs"""
		if nick is None:
			userInfo = discord.Embed(title = "Girls' Frontline Friend List", color = RandomColor())
			userInfo.set_footer(text = strfdelta(datetime.utcnow() - self.bot.uptime, 
				"Alive for {D} days {h} hours {m} minutes {s} seconds."), 
				icon_url = self.bot.user.avatar_url)
			db.execute("SELECT * FROM test ORDER BY uid")
			for record in db:
				userInfo.add_field(name = record[1], value = record[2])
			await self.bot.say(embed = userInfo)
		else:
			userInfo = discord.Embed(title = "Girls' Frontline User Info", color = RandomColor())
			userInfo.set_footer(text = strfdelta(datetime.utcnow() - self.bot.uptime, 
				"Alive for {D} days {h} hours {m} minutes {s} seconds."), 
				icon_url = self.bot.user.avatar_url)
			db.execute("SELECT * FROM test WHERE LOWER(name) = LOWER('{}')".format(nick))
			record = db.fetchone()
			userInfo.add_field(name = record[1], value = record[2])
			await self.bot.say(embed = userInfo)

	@gf.command(name = 'add', hidden = True)
	@checks.is_owner()
	async def add_user_to_list(self, nick, uid):
		db.execute("INSERT INTO test (name, uid) VALUES (%s, %s)", (nick, uid))
		conn.commit()
		await self.bot.say('Nick {} successfully added to the list.'.format(nick))

def setup(bot):
	bot.add_cog(Utility(bot))