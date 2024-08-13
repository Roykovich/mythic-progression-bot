import discord
import random
import re
from discord.ext import commands
from discord import app_commands

class CustomReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message: discord.Message):
        parsed = message.content.lower()

        if message.author.bot or message.author == self.bot.user:
            return
        
        if message.content.startswith(self.bot.command_prefix):
            return

        # Tradition.
        if re.search(r"([rg](ubén|uben|euben|uben|unerd|oy),? (arregla|repara|fixea|bichea|acomoda|mejora|upgradea|optimiza|soluciona|resuelve) [ts]u (maldit[ao]|put[ao]|verga?|estupid[ao])?\s?(mierda|vaina|verga|bot|perol|robot))", parsed):
            await message.add_reaction('😡')
            await message.channel.send('Está ocupado.')
            return

async def setup(bot):
    await bot.add_cog(CustomReactions(bot))