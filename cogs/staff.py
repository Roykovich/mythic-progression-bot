import discord
import requests
from discord.ext import commands
from discord import app_commands
from database.booster import register_user
from mythicsheets.booster import add_booster

# from settings import WP_SWINGS_CLIENT, WP_SWINGS_SECRET
# WP_SWINGS_URL = f'https://mythicprogression.com/wp-json/wsfw-route/v1/wallet/users?consumer_key={WP_SWINGS_CLIENT}&consumer_secret={WP_SWINGS_SECRET}'

class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='register', description='Busca un jugador en Raider.io')
    @app_commands.describe(email='email registered in mythicprogression.com')
    @app_commands.describe(user='discord user to register')
    @app_commands.describe(wallet_id='wallet id from mythicprogression.com')
    async def register(self, interaction: discord.Interaction, email: str, user: discord.User, wallet_id: str):
        # El server staff tiene que registrar el usuario con este comando para poder
        # agregar el id del monedero
        already_registered = register_user(email, user.id, wallet_id)

        if already_registered:
            await interaction.response.send_message(f'Usuario {user.mention} ya registrado.')
            return

        await add_booster(email, user.display_name, user.id)
        await interaction.response.send_message(f'Usuario {user.mention} registrado correctamente.\n**Email:** `{email}`\n**Wallet id:** `{wallet_id}`')

        
async def setup(bot):
    await bot.add_cog(Staff(bot))