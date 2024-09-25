import discord
from discord.ext import commands
from discord import app_commands

# en el test se llamaba CharacterList
class CharacterSelection(discord.ui.Select):
    def __init__(self, options):
        options = options
        super().__init__(placeholder='Selecciona un personaje', options=options, custom_id='character_list')

    async def callback(self, interaction: discord.Interaction):
        await self.view.selected_character(interaction=interaction, choice=self.values)
    

class CharactersList(discord.ui.View):
    character_selected = None 
    async def selected_character(self, interaction: discord.Interaction, choice):
        print(choice)
        self.character_selected = choice[0][1:]
        self.children[0].disabled = True
        await interaction.response.edit_message(view=self)
        self.stop()
