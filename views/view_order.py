import discord
import random # ! Esto es solo para emular el valor del raiderio
from database.applicants import is_already_applicated, apply_to_order, cancel_application, get_applications, update_applicants_fields
from utils.get_message import get_message

import settings
COMMAND_CHANNEL_ID = settings.COMMAND_CHANNEL_ID


def update_after_cancel(embed, order_id, role):
    applications = get_applications(order_id, role)
    update_applicants_fields(embed, applications, role)

# TODO cambiar la imagen a URL en imgur o algo
# * Ver como se aplica un for para las aplicaciones y ponerlo como un valor dinamico o usarlo directamente del valor del embed y solo agregarlo con un salto de linea
# * mover toda la DB a un archivo propio y hacer un archivo de funciones para las DB
# y que cada boton solo llame a estas funciones para que sea mas legible y modular
# Cuando se aplique un boton, se debe de actualizar el embed con los aplicantes (disabled cuando ya se selecciono los roles)
# crear tabla para los aplicantes aceptados con el id de la orden y el id del usuario y su rol

class OrderView(discord.ui.View):
    @discord.ui.button(label='Tank', emoji='<:Tank:1082086003113734214>', style=discord.ButtonStyle.grey)
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'tank'

        if is_already_applicated(order_id, user_id, role):
            print('ya aplicado')
            return

        apply_to_order(order_id, message_id, user_id, role, random.randint(600, 3500))
        applicants = get_applications(order_id, role)

        staff_message = await get_message(self.bot, message_id)
        embed = staff_message.embeds[0]
        
        update_applicants_fields(embed, applicants, role)
        
        await staff_message.edit(embed=embed, attachments=[])

    @discord.ui.button(label='Healer', emoji='<:Heal:1082086361936449627>', style=discord.ButtonStyle.grey)
    async def healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'healer'

        if is_already_applicated(order_id, user_id, role):
            print('ya aplicado')
            return

        apply_to_order(order_id, message_id, user_id, role, random.randint(600, 2500))
        applicants = get_applications(order_id, role)

        staff_message = await get_message(self.bot, message_id)
        embed = staff_message.embeds[0]
        
        update_applicants_fields(embed, applicants, role)
        
        await staff_message.edit(embed=embed, attachments=[])
        

    @discord.ui.button(label='Dps', emoji='<:dps:1257157322044608684>', style=discord.ButtonStyle.grey)
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'dps'

        if is_already_applicated(order_id, user_id, role):
            print('ya aplicado')
            return

        apply_to_order(order_id, message_id, user_id, role, random.randint(600, 2500))
        applicants = get_applications(order_id, role)

        staff_message = await get_message(self.bot, message_id)
        embed = staff_message.embeds[0]
        
        update_applicants_fields(embed, applicants, role)
        
        await staff_message.edit(embed=embed, attachments=[])
            

    @discord.ui.button(label='Team application', emoji='🔜', style=discord.ButtonStyle.blurple, row=1, disabled=True)
    async def team(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
    
    @discord.ui.button(label='Cancel', emoji='❌', style=discord.ButtonStyle.red, row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        user_id = interaction.user.id
        staff_message = await get_message(self.bot, self.message_id)
        embed = staff_message.embeds[0]

        if cancel_application(order_id, user_id) == 0:
            return
        
        update_after_cancel(embed, order_id, 'tank')
        update_after_cancel(embed, order_id, 'healer')
        update_after_cancel(embed, order_id, 'dps')

        await staff_message.edit(embed=embed, attachments=[])

        
        
        


        


        

