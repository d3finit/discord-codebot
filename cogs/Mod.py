import discord
import os
from discord.ext import commands

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# ==========================================================
# Moderator Cog
# ==========================================================
class Moderation(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None

	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		print("Moderation Cog loaded.")

	# Banned words listener
	@commands.Cog.listener('on_message')
	async def msgevent(self, message):
		if isinstance(message.channel, discord.channel.DMChannel) == False and message.author.bot != True:
			gname = message.guild.name.replace(" ", "")
			# Make sure this is the valid path to your file
			file = f"conf/server/{gname}/bannedwords.txt"
			with open(file) as f:
				lines = f.read().splitlines()
			for line in lines:
				if line.lower() in message.content.lower():
					linevalid = False
					for letter in letters:
						if letter in line:
							linevalid = True
							break
					if linevalid:	
						print("Banned word detected, removing...")
						await message.delete()

	# Commands
	# Mute command - Only users with the "Mod" role can use this
	@commands.command()
	@commands.has_role("Mod")
	async def mute(self, ctx, member: discord.Member):
		"""Mute users."""
		mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

		await member.add_roles(mutedRole)
	# await member.send(f"You have been muted on the server: {ctx.guild.name}")

		if member.nick == "None":
			embed = discord.Embed(title=f"Muted {member.name}", description=f"Sucessfully muted user {member.mention}",colour=discord.Colour.gold())
		
		else:
			embed = discord.Embed(title=f"Muted {member.nick}", description=f"Sucessfully muted user {member.mention}",colour=discord.Colour.gold())	
			
		await ctx.send(embed=embed)
		print(f"Muted user {member.mention}")


	
	
	# Unmute command - Only users with the "Mod" role can use this	
	@commands.command()
	@commands.has_role("Mod")
	async def unmute(self, ctx, member: discord.Member):
		"""Unmute users."""
		mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
		await member.remove_roles(mutedRole)
	# await member.send(f"You have been unmuted on the server: {ctx.guild.name}")

		if member.nick == "None":
			embed = discord.Embed(title=f"Unmuted {member.name}", description=f"Sucessfully unmuted user {member.mention}",colour=discord.Colour.gold())
		
		else:
			embed = discord.Embed(title=f"Unmuted {member.nick}", description=f"Sucessfully unmuted user {member.mention}",colour=discord.Colour.gold())	
		
		await ctx.send(embed=embed)
		print(f"Unmuted user {member.mention}")



	# purge command
	@commands.command(name='purge', help='Deletes x messages',aliases=['clear','nuke','wipe'])
	async def purge(ctx, amount=5):
		await ctx.channel.purge(limit=amount)
		
	
	# Lock command - Only users with the "Mod" role can use this
	@commands.command()
	@commands.has_role("Mod")
	async def lock(self, ctx, channel: discord.TextChannel):
		"""Locks channels."""
		channel = channel or ctx.channel
		overwrite = channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = False
		await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		await ctx.send('Channel locked.')

		
	
	# Unlock command - Only users with the "Mod" role can use this	
	@commands.command()
	@commands.has_role("Mod")
	async def unlock(self, ctx, channel: discord.TextChannel):
		"""Unlocks channels."""
		channel = channel or ctx.channel
		overwrite = channel.overwrites_for(ctx.guild.default_role)
		overwrite.send_messages = None
		await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		await ctx.send('Channel unlocked.')

	
	# Banword command - Only users with the "Admin" role can use this	
	@commands.command()
	@commands.has_role("Admin")
	async def banword(self, ctx, word):
		"""Bans words from being said on the server."""
		gname = ctx.guild.name.replace(" ", "")
		try:
			os.system(f"mkdir conf/server/{gname}")
		except Exception as e:
			print(e)
		# print("Made folder")
		try:
			os.system(f"touch conf/server/{gname}/bannedwords.txt")
		except Exception as e:
			print(e)
		# print("Made file")

		f = open(f"conf/server/{gname}/bannedwords.txt", "a")
		f.write(f"\n{word}")
		f.close()

		embed = discord.Embed(title=f"Added {word} to the banned words list.", description=f"Sucessfully banned {word}. Unban it with $unbanword {word}",colour=discord.Colour.red())	
		
		await ctx.send(embed=embed)
	
	
	# Unbanword command - Only users with the "Admin" role can use this
	@commands.command()
	@commands.has_role("Admin")
	async def unbanword(self, ctx, word):
		"""Unbans words from being said on the server."""
		gname = ctx.guild.name.replace(" ", "")
		# Make sure this is the valid path to your file
		file = f"conf/server/{gname}/bannedwords.txt"
		remove = word

		# Read in the file
		with open(file, "r") as f:
			filedata = f.read()

		# Replace the target string
		filedata = filedata.replace(remove, "")
		filedata = filedata.replace("\n","")

		# Write the file out again
		with open(file, "w") as f:
			f.write(filedata)

		embed = discord.Embed(title=f"Removed {word} from the banned words list.", description=f"Sucessfully unbanned {word}. Ban it with $banword {word}",colour=discord.Colour.red())	
		
		await ctx.send(embed=embed)







# Setup command - runs when the cog is loaded.
def setup(client):
	client.add_cog(Moderation(client))