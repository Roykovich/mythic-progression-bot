import discord
from discord.ext import commands
from discord import app_commands
from database.booster import get_booster_profile
from mythicsheets.booster import get_boosters
from utils.embed_booster_profile import embed_booster_profile

import settings

class Booster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='booster-profile', description='Profile de un booster')
    async def booster_profile(
        self,
        interaction: discord.Interaction,
    ):
        booster_characters = await get_booster_profile(interaction.user.id)
        booster_sheet = await get_boosters(user_id=str(interaction.user.id))
        
        if len(booster_characters) < 1:
            await interaction.response.send_message("No tienes personajes registrados", ephemeral=True)
            return    

        if not booster_sheet:
            await interaction.response.send_message(f"Aún no estas registrado. Pidele a un <@&{settings.ROLE_SERVER_STAFF_ID}> que te ayude a registrarte", ephemeral=True)
            return

        embed = await embed_booster_profile(
            booster=interaction.user,
            booster_points=booster_sheet[3],
            booster_rank=booster_sheet[4],
            characters=booster_characters
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
async def setup(bot):
    await bot.add_cog(Booster(bot))