import discord
from utils.get_message import get_message
from database.orders_misc_applicants import is_already_applicated, apply_to_misc_order, update_staff_applicants_fields_misc

import settings

class OrderMiscView(discord.ui.View):
    @discord.ui.button(label='Team application', emoji='🔜', style=discord.ButtonStyle.blurple, disabled=True)
    async def team(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
    
    @discord.ui.button(label='Apply', emoji='📝', style=discord.ButtonStyle.blurple)
    async def apply(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        order_name = self.order_name
        message_id = self.message_id
        booster_thread = self.thread_message
        user_id = interaction.user.id
        
        if is_already_applicated(order_id, user_id):
            print('ya aplicado')
            return
        
        await apply_to_misc_order(order_id, message_id, user_id)

        staff_message = await get_message(self.bot, message_id)
        embed = staff_message.embeds[0]

        update_staff_applicants_fields_misc(embed, order_id)

        await staff_message.edit(embed=embed, attachments=[])

        await interaction.user.send(f'<:quest:1107428715962572862> Has aplicado correctamente a `{order_name}`.\nEn unos instantes recibiras actualización a tu aplicación.')

    @discord.ui.button(label='Cancel', emoji='❌', style=discord.ButtonStyle.red, disabled=True)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
        return
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
