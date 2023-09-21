import discord
import os, json
from discord.ext import commands


# ==========================================================
# Misc Cog
# ==========================================================
class Misc(commands.Cog):
	def __init__(self, client):
		self.client = client
		self._last_member = None

	# Events
	@commands.Cog.listener()
	async def on_ready(self):
		print("Misc Cog loaded.")

	# Ping command
	@commands.command(name='ping', help="Checks the bot's ping.")
	async def ping(self, ctx):	
		await ctx.send('My ping is {0} ms'.format(str(commands.bot.latency * 1000)))




# Setup command - runs when the cog is loaded.
def setup(client):
	client.add_cog(Misc(client))