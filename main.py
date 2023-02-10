# main.py
import os
import os.path
from pytube import YouTube, Search
from disnake.ext import commands

bot = commands.Bot(
    command_prefix=';',
    test_guilds=[954588728226099260],
)


try:
	with open("TOKEN.txt") as f:
		TOKEN = f.read()
	if TOKEN == "":
		TOKEN = os.environ['DISCORD_TOKEN']
except:
	TOKEN = os.environ["DISCORD_TOKEN"]




@bot.slash_command(description="Plays from youtube")
async def play(inter, name:string):
	s = Search(file)
	s.results
	video = s.results[0].streams.filter(only_audio=True).first()
	destination = '.'
	out_file = video.download(output_path=destination)
	base, ext = os.path.splitext(out_file)
	new_file = "./file" + '.mp3'
	os.rename(out_file, new_file)
	vc = await channel.connect()
	vc.play(disnake.FFmpegPCMAudio('./file.mp3'), after=lambda e: print('done', e))
    await inter.response.send_message(f"Played {}")




bot.load_extension("cogs.ping") 


client.run(TOKEN)