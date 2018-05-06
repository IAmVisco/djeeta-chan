#assigning prefix and description
description = '''Multipurpose GBF oriented bot with useful commands and a bunch of emotes!'''
bot = commands.Bot(command_prefix = '~', description = description)


old code that i need to remake to avoid crashes with spaces overload
if ',' in choices:
	choices = choices.strip().split(',')
	await bot.say(":thinking:| I choose **" + random.choice(choices) + "!**")
else:
	await bot.say("Please check your input again. The format is ~choose <Option 1>, <Option 2>, etc.")

	
# FOR FUTURE USE
##############################################

@bot.command()
async def avatar(user: discord.Member):
	await bot.say(user.avatar_url)

@bot.command()
async def names(user : discord.User):
	await bot.say("Name " + user.name + " Nickname " + user.display_name)

# profanity filter
if message.server.id == casuals_id:
	for word in badWords:
		if word in message.content.lower():
			await bot.delete_message(message)
			await bot.send_message(message.channel, message.author.mention + " is a baka")
			await bot.add_roles(message.author, discord.utils.get(message.server.roles, name = 'muted'))
			await asyncio.sleep(300)
			await bot.remove_roles(message.author, discord.utils.get(message.server.roles, name = 'muted'))

# bless
@bot.command()
async def bless(user: discord.User):
	try:
		url = urllib.request.Request(user.avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
		with urllib.request.urlopen(url) as response, open(os.getcwd() + '/res/etc/image.png', 'wb') as out_file:
			data = response.read()
			out_file.write(data)
		size = 96, 96
		mask = Image.open(os.getcwd() + '/res/etc/mask.png').convert("L")
		im = Image.open(os.getcwd() + '/res/etc/image.png')
		out = ImageOps.fit(im, mask.size, centering = (0.5, 0.5))
		out.putalpha(mask)
		out.thumbnail(size, Image.ANTIALIAS)
		img_w, img_h = out.size
		bg = Image.open(os.getcwd() + '/res/etc/bless.png').convert("RGBA")
		offset = (160 - img_w // 2, 110 - img_h // 2)
		bg.alpha_composite(out, offset)
		bg.save(os.getcwd() + '/res/etc/bless_out.png')
		await bot.upload(os.getcwd() + '/res/etc/bless_out.png')
		os.remove(os.getcwd() + '/res/etc/bless_out.png')
		os.remove(os.getcwd() + '/res/etc/image.png')
	except:
		await bot.say("Check your input and try again. The format is ~bless <mention>")

@bot.command(pass_context = True)
async def record(ctx):
	the_file = open('logs/output.txt', 'w+')
	lst = []
	async for log in bot.logs_from(ctx.message.channel, limit=100000000000000):
		stringTime = log.timestamp.strftime("%Y-%m-%d %H:%M")
		msg = str(log.content.encode('UTF-8'))[2:-1]
		atr = str(log.author)
		template = '[{stringTime}] <{author}> {message}\n'
		lst.append(template.format(stringTime=stringTime, author=atr, message=msg))

	lst.reverse()
	try:
		for line in lst:
			if ('spoo.py' not in line):
				the_file.write(line.replace("<@208202505543221250>", "@Cas").replace("<@135259540722548736>", "@Ayaya").replace("\\n", "\n"))
			else:
				print(line)
	except:
		print(line)
	the_file.close()
	print('Done!')

# DEAD CODE REGION 
##############################################
trials based on excel table
@bot.command(description = 'I will show you current or future trial!')
async def trials():#arg:str):
	# if arg == "today":
	# 	await bot.say(str(datetime.now(timezone('Europe/Samara')).strftime("%d of %b (today) - ")) + str(sheet.row[datetime.now(timezone('Europe/Samara')).day-1][0]) + " Trial")
	# elif arg.isdigit():
	# 	await bot.say(arg + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[int(arg)-1][0]) + " Trial")
	# elif arg.isalpha():    
	# 	for record in range(datetime.now(timezone('Europe/Samara')).day, len(sheet.column[1])):
	# 		if arg.lower() == sheet.row[int(record)][0].lower():
	# 			await bot.say(str(record+1) + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[record][0]) + " Trial")
	# 			break
	# else:
	# 	await bot.say("Please check your input and try again. Use ~help for more info.")
	await bot.say("I'm too lazy to write good code for this one.")
#showdowns too
@bot.command(description = 'I will show you current or future showdown!')

#revealing true self
@bot.command(pass_context = True, description = 'I will use my powers to reveal true self of the chosen one!')
async def reveal(ctx, *, userName):
	if userName[1] == "@":
		user = discord.utils.get(ctx.message.server.members, mention = userName)
	else:
		user = discord.utils.get(ctx.message.server.members, display_name = userName)
	await bot.say("I'm sure it's **" + user.name + "**!")

async def showdowns():#arg:str):
	# if arg == "today":
	# 	await bot.say(str(datetime.now(timezone('Europe/Samara')).strftime("%d of %b (today) - ")) + str(sheet.row[datetime.now(timezone('Europe/Samara')).day-1][1]) + " Showdown")
	# elif arg.isdigit():
	# 	await bot.say(arg + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[int(arg)-1][1]) + " Showdown")
	# elif arg.isalpha():    
	# 	for record in range(datetime.now(timezone('Europe/Samara')).day, len(sheet.column[1])):
	# 		if arg.lower() == sheet.row[int(record)][1].lower():
	# 			await bot.say(str(record+1) + str(datetime.now(timezone('Europe/Samara')).strftime(" of %b - ")) + str(sheet.row[record][1]) + " showdown")
	# 			break
	# else:
	# 	await bot.say("Please check your input and try again. Use ~help for more info.")
	await bot.say("I'm too lazy to write good code for this one.") 

@bot.event
async def on_message(message):
	await bot.process_commands(message)	

(message.author.id == 185069144184455168) and 
pepeGun = discord.utils.get(message.server.emojis, name = 'pepeGun')
if not pepeGun == None:
	for wrong_name in wrong_names:
		if wrong_name.lower() in message.content.lower():
			await bot.send_message(message.channel, "It's time to stop " + str(pepeGun) +"\nhttps://thumbs.gfycat.com/AdmirableShadyCur-size_restricted.gif")
			break

insults
if message.author.id in victim_list:
	if (message.server.id != "301829994567434241"):
		pool = ["🇱", "🇪", "🇼", "🇩", "🍆"]
		pool = ["🇸","🇹","🇺","🇵","🇮","🇩"]
		if message.author.id in victim_list and random.randint(1,100) == 1:
			for letter in pool:
				await bot.add_reaction(message, letter)
		if (random.randint(1,100) == 1):
			await bot.send_message(message.channel, message.author.mention + random.choice(insults_list))

Beaver is ded MingLow
if beaver <= 0 and "beaver" in message.content.lower() and ("dead" in message.content.lower() or "ded" in message.content.lower()):
	await bot.send_message(message.channel, "MingLow")
	beaver = 10

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
