import discord
import random # ! Esto es solo para emular el valor del raiderio
from database.applicants import is_already_applicated, apply_to_order, cancel_application, get_applications, update_applicants_fields
from database.orders import check_order_full, get_order_info
from utils.embed_order import order_created_embed

import settings
COMMAND_CHANNEL_ID = settings.COMMAND_CHANNEL_ID


# TODO cambiar la imagen a URL en imgur o algo
# * Ver como se aplica un for para las aplicaciones y ponerlo como un valor dinamico o usarlo directamente del valor del embed y solo agregarlo con un salto de linea
# * mover toda la DB a un archivo propio y hacer un archivo de funciones para las DB
# * y que cada boton solo llame a estas funciones para que sea mas legible y modular
# Cuando se aplique un boton, se debe de actualizar el embed con los aplicantes (disabled cuando ya se selecciono los roles)
# * crear tabla para los aplicantes aceptados con el id de la orden y el id del usuario y su rol

class OrderCommandView(discord.ui.View):
    @discord.ui.button(label='Tank full', emoji='<:Tank:1082086003113734214>', style=discord.ButtonStyle.grey, disabled=True)
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'tank'
        ...

    @discord.ui.button(label='Healer full', emoji='<:Heal:1082086361936449627>', style=discord.ButtonStyle.grey, disabled=True)
    async def healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'healer'
        ...
        

    @discord.ui.button(label='Dps full', emoji='<:dps:1257157322044608684>', style=discord.ButtonStyle.grey, disabled=True)
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'dps'
        ...
            

    @discord.ui.button(label='Complete Selection', emoji='✅', style=discord.ButtonStyle.success, row=1)
    async def team(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff_channel = self.bot.get_channel(COMMAND_CHANNEL_ID)
        boosters = check_order_full(self.order_id)

        if boosters:
            await interaction.response.send_message('Orden completa', ephemeral=True)
            thread = await staff_channel.create_thread(name=f'Order - {self.order_id}', reason='Orden Iniciada', invitable=False)
            order_info = get_order_info(self.order_id)

            tags = ''

            for booster_id in boosters:
                tags += f'<@{booster_id}> '

            tags += f'\n<@&861688529637474385>'

            embed = order_created_embed(order_info, boosters)

            await thread.send(f'Orden [{self.order_id}] iniciada\n\n{tags}', embed=embed)
            return
        
        await interaction.response.send_message('La orden no está completa', ephemeral=True)
        
    
