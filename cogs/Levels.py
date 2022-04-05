import discord
import os, json
from discord.ext import commands


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
		if isinstance(message.channel, discord.channel.DMChannel) == False and message.author.bot == False:
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


	@commands.command(name='stats', help="Gets a user's stats")
	async def stats(ctx, member: discord.Member):
		print(f"{member.name}#{member.discriminator}")
		if os.path.exists(f'conf/user/{member.name}#{member.discriminator}.json') == True:
			filename = f'conf/user/{member.name}#{member.discriminator}.json'
			with open(filename, 'r') as f:
				data = json.load(f)
				xplevel = data["levels"]["xp"]
				statlevel = str(data["levels"]["level"])
			if member.nick == "None":
				embed = discord.Embed(title=f"**Stats for {member.name}**", description=f"XP: {str(xplevel)}.\nLevel: {str(statlevel)}.",colour=discord.Colour.gold())
		
			else:
				embed = discord.Embed(title=f"**Stats for {member.nick}**", description=f"XP: {str(xplevel)}.\nLevel: {str(statlevel)}.",colour=discord.Colour.gold())	
		
			await ctx.send(embed=embed)
		# print(f"Unmuted user {member.mention}")




# Setup command - runs when the cog is loaded.
def setup(client):
	client.add_cog(Levels(client))