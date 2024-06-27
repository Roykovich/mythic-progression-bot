import discord
import requests
from discord.ext import commands
from discord import app_commands

import settings

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='my!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} ha iniciado correctamente\n')
        print('<-------------------------------------------->\n')

        for cog_file in settings.COGS_DIR.glob('*.py'):
            if cog_file != "__init__.py":
                await bot.load_extension(f'cogs.{cog_file.name[:-3]}')
                print(f'[+] Cog {cog_file.name[:-3]} cargado correctamente')

        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)

    bot.run(settings.TOKEN)

if __name__ == '__main__':
    main()