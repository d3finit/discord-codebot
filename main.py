# main.py
import os
import os.path
import json, asyncio

import discord
from discord.ext import commands 
from gtts import gTTS # Text to speech

client = discord.Client()
engine = pyttsx3.init()

try:
	with open("TOKEN.txt") as f:
		TOKEN = f.read()
	if TOKEN == "":
		TOKEN = os.environ['DISCORD_TOKEN']
except:
	TOKEN = os.environ["DISCORD_TOKEN"]

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
	await bot.change_presence(activity=discord.Game(name="$help | discord.gg/7Y9fZEN58J"))

	print("Bot is online")



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
	voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
	if todo == "play":
		if file != None:
			audio_source = discord.FFmpegPCMAudio("conf/assets/" + file + ".mp3")
			if not voice_client.is_playing():
				voice_client.play(audio_source, after=None)
				await ctx.send(f'Playing {file}')
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
		songs = os.listdir("./conf/assets")
		songstr = "Songs: \n  "
		for i in range(len(songs)):
			songstr = songstr + str(songs[i])[:-4] +"\n  "
		await ctx.send(songstr)
		



@bot.listen('on_voice_state_update')
async def on_voice_state_update(member, before, after): 
	if not member.bot and after != None and before.channel != after.channel:
		try:
			voice_client = await after.channel.connect() # Thing
			myobj = gTTS(text="Hi", lang="en", slow=False)
			myobj.save("speech.mp3")
			engine.runAndWait()
			audio_source = discord.FFmpegPCMAudio('speech.mp3')
			if not voice_client.is_playing():
				voice_client.play(audio_source, after=None)
				
		except:
			pass
	if after is None:
		before.channel.disconnect()



for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f"cogs.{filename[:-3]}")
		
bot.run(TOKEN)