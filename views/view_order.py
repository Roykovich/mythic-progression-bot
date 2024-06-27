import discord

class MusicView(discord.ui.View):
    @discord.ui.button(label='Aplicar solo', emoji='', style=discord.ButtonStyle.blurple)
    async def a(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...

    @discord.ui.button(label='Aplicar Team', emoji='', style=discord.ButtonStyle.red)
    async def b(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...

    @discord.ui.button(label='Cancelar Aplicación', emoji='', style=discord.ButtonStyle.green)
    async def c(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
