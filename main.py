# main.py
import os
import os.path
import json, asyncio

import discord
from discord.ext import commands 
from gtts import gTTS
from pytube import YouTube, Search

client = discord.Client()

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
	no_category = 'Other'
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
	await bot.change_presence(activity=discord.Game(name="$help"))

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

@bot.command(aliases=['m'],name='music', help='Allows you to play mp3s.')
async def music(ctx, input1 = None, file = None):
	guild = ctx.guild
	voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
	if input1 == "play":
		if file is not None:
			s = Search(file)
			s.results
			video = s.results[0].streams.filter(only_audio=True).first()
			destination = '.'
			out_file = video.download(output_path=destination)
			base, ext = os.path.splitext(out_file)
			new_file = "file" + '.mp3'
			os.rename(out_file, new_file)

			audio_source = discord.FFmpegPCMAudio("./file.mp3")
			if not voice_client.is_playing():
				voice_client.play(audio_source, after=None)
				await ctx.send(f'Playing {file}')
			else:		
				await ctx.send(f'Failed to play {file}.mp3. Try running $music stop then trying again.')

	elif input1 == "stop":
		voice_client.stop()		
		await ctx.send(f'Stopped music.')
	elif input1 == "pause":
		voice_client.pause()
		await ctx.send(f'Paused music')
	elif input1 == "resume":
		voice_client.resume()
		await ctx.send(f'Resumed music')



@bot.listen('on_voice_state_update')
async def on_voice_state_update(member, before, after): 
	if not member.bot and after != None and before.channel != after.channel:
		print("User joined voice")
		try:
			voice_client = await after.channel.connect() # Thing
			myobj = gTTS(text=f"{member.display_name} is now connected.", lang="en", slow=False)
			myobj.save("speech.mp3")
			audio_source = discord.FFmpegPCMAudio('speech.mp3')
			if not voice_client.is_playing():
				voice_client.play(audio_source, after=None)
			while voice_client.is_playing():
				pass
			await voice_client.disconnect()
				
		except:
			pass
	if not member.bot and before.channel is not after.channel and after.channel is None:
		print("User left voice")
		try:
			voice_client = await before.channel.connect() # Thing
			myobj = gTTS(text=f"{member.display_name} has disconnected.", lang="en", slow=False)
			myobj.save("speech.mp3")
			audio_source = discord.FFmpegPCMAudio('speech.mp3')
			if not voice_client.is_playing():
				voice_client.play(audio_source, after=None)
			while voice_client.is_playing():
				pass
			await voice_client.disconnect()
				
		except:
			pass



for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		bot.load_extension(f"cogs.{filename[:-3]}")
		
bot.run(TOKEN)