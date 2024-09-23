import discord
from database.booster import register_booster_character

from utils.get_message import get_message

class RegisterRaiderioView(discord.ui.View):
    @discord.ui.button(label='Registrar', style=discord.ButtonStyle.green)
    async def register(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

        if interaction.user.id != self.booster_id:
            await interaction.followup.send('No puedes registrar a un personaje que no es tuyo', ephemeral=True)
            return

        pj = self.pj
        booster_id = self.booster_id
        await register_booster_character(booster_id, pj)

        self.clear_items()
        await self.original_message.edit(content='## ✅ Registro realizado', view=self)
        await interaction.followup.send('Personaje registrado con éxito', ephemeral=True)

    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.booster_id:
            await interaction.followup.send('No puedes hacer esto,', ephemeral=True)
            return

        self.clear_items()
        await self.original_message.edit(content='## ❌ Registro cancelado', view=self)
        await interaction.response.send_message('Registro cancelado', ephemeral=True)
        