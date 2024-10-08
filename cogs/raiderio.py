import discord
import requests
from discord.ext import commands
from discord import app_commands

from utils.load_region_servers import realms_autocomplete
from utils.embed_raiderio import raiderio_profile

from views.register_raiderio import RegisterRaiderioView
from utils.raiderio import get_raiderio_profile


class Raiderio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='search-raiderio', description='Busca un jugador en Raider.io')
    @app_commands.choices(region=[
        app_commands.Choice(name='us', value="us")
    ])
    @app_commands.autocomplete(realm=realms_autocomplete)
    @app_commands.describe(name="Nombre del jugador")
    async def raiderioslash(self, interaction: discord.Interaction, region: app_commands.Choice[str], realm: str, name: str):
        pj = get_raiderio_profile(region.value, realm.replace(" ", "%20"), name)

        if "error" in pj:
            await interaction.response.send_message('No se ha encontrado al personaje. Asegurate que escribiste bien el nombre', ephemeral=True)
            return
        
        embed = raiderio_profile(pj)
        await interaction.response.send_message(f'Buscando a {name} en Raider.io')
        await interaction.channel.send(content='', embed=embed, ephemeral=True)


    @app_commands.command(name='register-raiderio', description='Registrar un pj con Raider.io')
    @app_commands.choices(region=[
        app_commands.Choice(name='us', value="us")
    ])
    @app_commands.autocomplete(realm=realms_autocomplete)
    @app_commands.describe(name="Nombre del jugador")
    async def register_raiderio(
        self,
        interaction: discord.Interaction,
        region: app_commands.Choice[str],
        realm: str,
        name: str
    ):
        pj = get_raiderio_profile(region.value, realm.replace(" ", "%20"), name)

        if "error" in pj:
            await interaction.response.send_message('No se ha encontrado al personaje. Asegurate que escribiste bien el nombre', ephemeral=True)
            return

        embed = raiderio_profile(pj)
        view = RegisterRaiderioView(timeout=None)
        view.booster_id = interaction.user.id
        view.bot = self.bot
        view.pj = pj

        await interaction.response.send_message(content='', embed=embed, view=view, ephemeral=True)

        view.original_message = await interaction.original_response()

async def setup(bot):
    await bot.add_cog(Raiderio(bot))