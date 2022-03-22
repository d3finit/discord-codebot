# bot.py
import os
import os.path
import random, json

import discord
import asyncio
from discord.ext import commands


client = discord.Client()
with open("TOKEN.txt") as f:
	TOKEN = f.read()

# print(TOKEN)
# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
	no_category = 'Commands'
)

# Create the bot and pass it the modified help_command
bot = commands.Bot(
	command_prefix = commands.when_mentioned_or('$'),
	description = "=== CodeBot Help ===",
	help_command = help_command
)

@bot.event
async def on_ready():
	# Setting `Playing ` status
	await bot.change_presence(activity=discord.Game(name="$help | github.com/CodeDude404/discord-codebot"))

	print("ONLINE NOW ;)")

	 # Setting `Streaming ` status
	 # await bot.change_presence(activity=discord.Streaming(name="My Stream", url="google.com"))



		
# ==========================================================
# Mod FEatures
# ==========================================================
@bot.command(name='mute', help='Mutes user.')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	await member.add_roles(mutedRole)
	# await member.send(f"You have been muted on the server: {ctx.guild.name}")

	if member.nick == "None":
		embed = discord.Embed(title=f"Muted {member.name}", description=f"Sucessfully muted user {member.mention}",colour=discord.Colour.gold())
		
	else:
		embed = discord.Embed(title=f"Muted {member.nick}", description=f"Sucessfully muted user {member.mention}",colour=discord.Colour.gold())	
		
	await ctx.send(embed=embed)
	print(f"Muted user {member.mention}")





@bot.command(name='unmute', help='Unmutes user.')
async def unmute(ctx, member: discord.Member):
	mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

	await member.remove_roles(mutedRole)
	# await member.send(f"You have been unmuted on the server: {ctx.guild.name}")

	if member.nick == "None":
		embed = discord.Embed(title=f"Unmuted {member.name}", description=f"Sucessfully unmuted user {member.mention}",colour=discord.Colour.gold())
		
	else:
		embed = discord.Embed(title=f"Unmuted {member.nick}", description=f"Sucessfully unmuted user {member.mention}",colour=discord.Colour.gold())	
		
	await ctx.send(embed=embed)
	print(f"Unmuted user {member.mention}")






@bot.command(name='lock', help='Locks channel.')
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
	channel = channel or ctx.channel
	overwrite = channel.overwrites_for(ctx.guild.default_role)
	overwrite.send_messages = False
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
	await ctx.send('Channel locked.')

@bot.command(name='unlock', help='Unlocks channel.')
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
	channel = channel or ctx.channel
	overwrite = channel.overwrites_for(ctx.guild.default_role)
	overwrite.send_messages = True
	await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
	await ctx.send('Channel unlocked.')


# purge command
@bot.command(name='purge', help='Deletes x messages',aliases=['clear','nuke','wipe'])
async def purge(ctx, amount=5):
	await ctx.channel.purge(limit=amount)


# ==========================================================
# Music player stuff
# ==========================================================


@bot.command(name='join', help='Joins the voice channel that the user is in.')
async def join(ctx):
	channel = ctx.author.voice.channel;
	await channel.connect();
	await ctx.send('Joined voice.');
	
@bot.command(name='leave', help='Leaves the voice channel that the user is in.')
async def leave(ctx):
	await ctx.voice_client.disconnect();
	await ctx.send('Left voice.');

@bot.command(aliases=['m'],name='music', help='Allows you to play mp3s. ($music list to see all songs, $m <arg> is the same thing.)')
async def music(ctx, todo = None, file = None):
	guild = ctx.guild
	voice_client: discord.VoiceClient = 		discord.utils.get(bot.voice_clients, guild=guild)
	if todo == "play":
		if file != None:
			audio_source = discord.FFmpegPCMAudio("assets/" + file + ".mp3")
			if not voice_client.is_playing():
				voice_client.play(audio_source, after=None)
				await ctx.send(f'Playing {file}.mp3')
			else:		
				await ctx.send(f'Failed to play {file}.mp3. Try running $music stop then trying again.')

	elif todo == "stop":
		voice_client.stop()		
		await ctx.send(f'Stopped music.')
	elif todo == "pause":
		voice_client.pause()
		await ctx.send(f'Paused music')
	elif todo == "resume":
		voice_client.resume()
		await ctx.send(f'Resumed music')
	elif todo == "list":
		songs = os.listdir("./assets")
		songstr = "Songs: \n  "
		for i in range(len(songs)):
			songstr = songstr + songs[i] +"\n  "
		await ctx.send(songstr)
		

# ==========================================================
# Stats command
# ==========================================================

@bot.command(name='stats', help="Gets a user's stats")
async def stats(ctx, member: discord.Member):
	print(f"{member.name}#{member.discriminator}")
	if os.path.exists(f'userinfo/{member.name}#{member.discriminator}.json') == True:
		filename = f'userinfo/{member.name}#{member.discriminator}.json'
		with open(filename, 'r') as f:
			data = json.load(f)
			xplevel = data["levels"]["xp"]
			statlevel = str(data["levels"]["level"])
		if member.nick == "None":
			embed = discord.Embed(title=f"**Stats for {member.name}**", description=f"XP: `{str(xplevel)}`.\nLevel: `{statlevel}`.",colour=discord.Colour.gold())
		
		else:
			embed = discord.Embed(title=f"**Stats for {member.nick}**", description=f"XP level: `{str(xplevel)}`.",colour=discord.Colour.gold())	
		
		await ctx.send(embed=embed)
		# print(f"Unmuted user {member.mention}")




		
# ==========================================================
# Reply to DM's
# ==========================================================

@bot.listen('on_message')
async def msgevent(message):
	if isinstance(message.channel, discord.channel.DMChannel) and message.author != bot.user:
		if message.content == 'repo':
			await message.channel.send('View our GitHub at github.com/CodeDude404/discord-codebot')
		elif message.content == 'help':
			await message.channel.send('Use $help in a server with the bot in it too see the help menu.')

@bot.listen('on_voice_state_update')
async def voiceevent(member, before, after): 
	if after.channel.id == before.channel.id and not member.bot: 
		voice_client = await channel.connect()

# ==========================================================
# Ping command
# ==========================================================
@bot.command(name='ping', help="Checks the bot's ping.")
async def ping(ctx):
	guild = ctx.guild		
	await ctx.send('My ping is {0} ms'.format(str(bot.latency * 1000)))

# ==========================================================
# Levels Code
# ==========================================================
@bot.listen('on_message')
async def msgevent(message):
	if isinstance(message.channel, discord.channel.DMChannel) == False and message.author != bot.user:
	# print(str(message.author) + " is trying to register")
			# print(os.path.exists(f'userinfo/{message.author}.json'))
		if os.path.exists(f'userinfo/{message.author}.json') == True:
			filename = f'userinfo/{message.author}.json'
			with open(filename, 'r') as f:
				data = json.load(f)
				if data["levels"]["xp"] + len(message.content) >= data["levels"]["level"]+1*8:
					data["levels"]["xp"] = data["levels"]["xp"] + len(message.content)
					data["levels"]["xp"] = data["levels"]["xp"] -data["levels"]["level"]+1*8
					await message.channel.send(f"GG {str(message.author)}, you advanced to level {str(data['levels']['level'])}!")
				else:
					data["levels"]["xp"] = data["levels"]["xp"] + len(message.content) # update xp level
				os.remove(filename)
			with open(filename, 'w') as f:
				json.dump(data, f, indent=4)
 
		else:
			if os.path.exists(f'userinfo/{message.author}.json') == False:
				f = open(f'userinfo/{message.author}.json', "w")
				f.write(open("userinfo/default.json", "r").read())
				f.close()
		
bot.run(TOKEN)