import discord
import random # ! Esto es solo para emular el valor del raiderio
from database.applicants import is_already_applicated, apply_to_order, cancel_application, get_applications, update_applicants_fields

import settings
COMMAND_CHANNEL_ID = settings.COMMAND_CHANNEL_ID


def update_after_cancel(embed, order_id, role):
    applications = get_applications(order_id, role)
    update_applicants_fields(embed, applications, role)

async def get_message(bot, message_id):
    channel = bot.get_channel(COMMAND_CHANNEL_ID)
    message = await channel.fetch_message(message_id)

    return message

# TODO cambiar la imagen a URL en imgur o algo
# * Ver como se aplica un for para las aplicaciones y ponerlo como un valor dinamico o usarlo directamente del valor del embed y solo agregarlo con un salto de linea
# * mover toda la DB a un archivo propio y hacer un archivo de funciones para las DB
# y que cada boton solo llame a estas funciones para que sea mas legible y modular
# Cuando se aplique un boton, se debe de actualizar el embed con los aplicantes (disabled cuando ya se selecciono los roles)
# crear tabla para los aplicantes aceptados con el id de la orden y el id del usuario y su rol

class OrderCommandView(discord.ui.View):
    @discord.ui.button(label='Tank full', emoji='<:Tank:1082086003113734214>', style=discord.ButtonStyle.grey, disabled=True)
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'tank'
        ...

    @discord.ui.button(label='Healer', emoji='<:Heal:1082086361936449627>', style=discord.ButtonStyle.grey, disabled=True)
    async def healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'healer'
        ...
        

    @discord.ui.button(label='Dps', emoji='<:dps:1257157322044608684>', style=discord.ButtonStyle.grey, disabled=True)
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'dps'
        ...
            

    @discord.ui.button(label='Complete Selection', emoji='✅', style=discord.ButtonStyle.success, row=1, disabled=True)
    async def team(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        ...
    
