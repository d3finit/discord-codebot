import discord
import os, json
from discord.ext import commands

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# ==========================================================
# Levels Cog
# ==========================================================
class Levels(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None

	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		print("Levels Cog loaded.")


	@commands.Cog.listener()
	async def on_message(self, message):
		if isinstance(message.channel, discord.channel.DMChannel) == False and message.author != commands.bot.user:
		# print(str(message.author) + " is trying to register")
				# print(os.path.exists(f'conf/user/{message.author}.json'))
			if os.path.exists(f'conf/user/{message.author}.json') == True:
				filename = f'conf/user/{message.author}.json'
				with open(filename, 'r') as f:
					data = json.load(f)
				#print(data)

				data["levels"]["xp"] = len(message.content) + data["levels"]["xp"]
				print(f"granted {str(len(message.content))} xp to {str(message.author)}")
				if data["levels"]["xp"] >= (data["levels"]["level"]+1)*100:
					data["levels"]["xp"] = data["levels"]["xp"] - (data["levels"]["level"]+1)*100
					data["levels"]["level"] = data["levels"]["level"] + 1
					
					await message.channel.send(f"GG {str(message.author.mention)}, you advanced to level {str(data['levels']['level'])}!")
				os.remove(filename)

				with open(filename, 'w') as f:
					json.dump(data, f, indent=4)
 
			else:
				if os.path.exists(f'conf/user/{message.author}.json') == False:
					f = open(f'conf/user/{message.author}.json', "w")
					f.write(open("conf/user/default.json", "r").read())
					f.close()





# Setup command - runs when the cog is loaded.
def setup(client):
	client.add_cog(Levels(client))