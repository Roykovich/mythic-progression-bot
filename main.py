import discord
from discord.ext import commands
from discord import app_commands

import settings
import database.main as db

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='my!', intents=intents)

    @bot.event
    async def on_ready():
        # print(f'{bot.user} ha iniciado correctamente\n')
        # print('<-------------------------------------------->\n')
        print('''
|  \/  |     | | | |   (_)                             
| \  / |_   _| |_| |__  _  ___                         
| |\/| | | | | __| '_ \| |/ __|                        
| |  | | |_| | |_| | | | | (__                         
|_|__|_|\__, |\__|_| |_|_|\___|          _             
|  __ \  __/ |                          (_)            
| |__) ||___/__   __ _ _ __ ___  ___ ___ _  ___  _ __  
|  ___/ '__/ _ \ / _` | '__/ _ \/ __/ __| |/ _ \| '_ \ 
| |   | | | (_) | (_| | | |  __/\__ \__ \ | (_) | | | |
|_|__ |_|  \___/ \__, |_|  \___||___/___/_|\___/|_| |_|
|  _ \      | |   __/ |                                
| |_) | ___ | |_ |___/                                 
|  _ < / _ \| __|                                      
| |_) | (_) | |_                                       
|____/ \___/ \__|    
        ''')

        for cog_file in settings.COGS_DIR.glob('*.py'):
            if cog_file != "__init__.py":
                await bot.load_extension(f'cogs.{cog_file.name[:-3]}')
                print(f'[+] Cog {cog_file.name[:-3]} cargado correctamente')

        bot.tree.copy_global_to(guild=settings.GUILD_ID)
        await bot.tree.sync(guild=settings.GUILD_ID)

        db.create_tables()


    bot.run(settings.TOKEN)

if __name__ == '__main__':
    main()