import discord
import random # ! Esto es solo para emular el valor del raiderio
from database.applicants import is_already_applicated, apply_to_order, cancel_application, update_staff_applicants_fields, update_applicants_fields
from database.orders import check_if_booster_is_already_in_order
from utils.get_message import get_message

import settings
COMMAND_CHANNEL_ID = settings.COMMAND_CHANNEL_ID

class OrderView(discord.ui.View):
    @discord.ui.button(label='Tank', emoji='<:tank:1270969225871360010>', style=discord.ButtonStyle.grey)
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        order_name = self.order_name
        message_id = self.message_id
        booster_thread = self.thread_message
        user_id = interaction.user.id
        role = 'tank'

        if is_already_applicated(order_id, user_id, role):
            print('ya aplicado')
            return

        await apply_to_order(order_id, message_id, user_id, role, random.randint(600, 3500))

        staff_message = await get_message(self.bot, message_id)
        booster_message = await get_message(self.bot, booster_thread, booster_thread)
        embed = staff_message.embeds[0]
        booster_embed = booster_message.embeds[0]
        
        update_staff_applicants_fields(embed, order_id)
        update_applicants_fields(booster_embed, role, order_id)
        
        await staff_message.edit(embed=embed, attachments=[])
        await booster_message.edit(embed=booster_embed, attachments=[])

        await interaction.user.send(f'Has aplicado correctamente a `{order_name}` como <:tank:1270969225871360010> **{role}**.\nEn unos instantes recibiras actualización a tu aplicación.')
        

    @discord.ui.button(label='Healer', emoji='<:Heal:1082086361936449627>', style=discord.ButtonStyle.grey)
    async def healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        order_name = self.order_name
        message_id = self.message_id
        booster_thread = self.thread_message
        user_id = interaction.user.id
        role = 'healer'

        if is_already_applicated(order_id, user_id, role):
            print('ya aplicado')
            return

        await apply_to_order(order_id, message_id, user_id, role, random.randint(600, 2500))

        staff_message = await get_message(self.bot, message_id)
        booster_message = await get_message(self.bot, booster_thread, booster_thread)
        embed = staff_message.embeds[0]
        booster_embed = booster_message.embeds[0]
        
        update_staff_applicants_fields(embed, order_id)
        update_applicants_fields(booster_embed, role, order_id)
        
        await staff_message.edit(embed=embed, attachments=[])
        await booster_message.edit(embed=booster_embed, attachments=[])
        
        await interaction.user.send(f'Has aplicado correctamente a `{order_name}` como <:Heal:1082086361936449627> **{role}**.\nEn unos instantes recibiras actualización a tu aplicación.')
    

    @discord.ui.button(label='Dps', emoji='<:dps:1257157322044608684>', style=discord.ButtonStyle.grey)
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        order_name = self.order_name
        message_id = self.message_id
        booster_thread = self.thread_message
        user_id = interaction.user.id
        role = 'dps'

        if is_already_applicated(order_id, user_id, role):
            print('ya aplicado')
            return

        await apply_to_order(order_id, message_id, user_id, role, random.randint(600, 2500))

        staff_message = await get_message(self.bot, message_id)
        booster_message = await get_message(self.bot, booster_thread, booster_thread)
        embed = staff_message.embeds[0]
        booster_embed = booster_message.embeds[0]
        
        update_staff_applicants_fields(embed, order_id)
        update_applicants_fields(booster_embed, role, order_id)
        
        await staff_message.edit(embed=embed, attachments=[])
        await booster_message.edit(embed=booster_embed, attachments=[])
            
        await interaction.user.send(f'Has aplicado correctamente a `{order_name}` como <:dps:1257157322044608684> **{role}**.\nEn unos instantes recibiras actualización a tu aplicación.')


    @discord.ui.button(label='Team application', emoji='🔜', style=discord.ButtonStyle.blurple, row=1, disabled=True)
    async def team(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
    
    @discord.ui.button(label='Cancel', emoji='❌', style=discord.ButtonStyle.red, row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        order_id = self.order_id
        user_id = interaction.user.id
        staff_message = await get_message(self.bot, self.message_id)
        embed = staff_message.embeds[0]

        if cancel_application(order_id, user_id) == 0:
            await interaction.response.send_message('No has aplicado a esta orden.', ephemeral=True)
            return
        
        update_staff_applicants_fields(embed, order_id)

        # Si el Booster estaba aceptado en la orden, aqui nos aseguramos de eliminarlo del embed
        if check_if_booster_is_already_in_order(order_id, user_id) == 1:
            update_staff_applicants_fields(embed, order_id, accepted=True, booster=user_id)
            # Aqui podriamos agregar algo que avise al creador de la orden que alguien se le fue de la orden

        await staff_message.edit(embed=embed, attachments=[])
        await interaction.response.send_message('Has cancelado tu aplicación correctamente.', ephemeral=True)

        
        
        


        


        

