import discord
import requests
from discord.ext import commands
from discord import app_commands

from utils.load_region_servers import realms_autocomplete

URL = "https://raider.io/api/v1/characters/profile?region=us&realm=Bleeding%20Hollow&name="
URL2 = "https://raider.io/api/v1/characters/profile?"
MYTHIC_SUFIX = "&fields=mythic_plus_scores_by_season%3Acurrent,gear"

class Raiderio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='raiderio', description='Busca un jugador en Raider.io')
    @app_commands.choices(region=[
        app_commands.Choice(name='us', value="us")
    ])
    @app_commands.autocomplete(realm=realms_autocomplete)
    @app_commands.describe(name="Nombre del jugador")
    async def raiderioslash(self, interaction: discord.Interaction, region: app_commands.Choice[str], realm: str, name: str):
        response = requests.get(f'{URL2}region={region.value}&realm={realm.replace(" ", "%20")}&name={name}{MYTHIC_SUFIX}').json()
        print(response)
        await interaction.response.send_message(f'Buscando a {name} en Raider.io\n**raza:** {response['race']}\n**clase:** {response['class']}\n**Especializacion activa:** {response['active_spec_name']}\n')
        await interaction.channel.send(f'**Puntuacion de mazmorras:** {response["mythic_plus_scores_by_season"][0]["scores"]["all"]}\n**Tanque:** {response["mythic_plus_scores_by_season"][0]["scores"]["tank"]}\n**Sanador:** {response["mythic_plus_scores_by_season"][0]["scores"]["healer"]}\n**DPS:** {response["mythic_plus_scores_by_season"][0]["scores"]["dps"]}\n**ilvl:** {response["gear"]["item_level_equipped"]}')

        # embed = discord.Embed()


async def setup(bot):
    await bot.add_cog(Raiderio(bot))