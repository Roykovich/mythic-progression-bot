import discord
from database.orders_dungeon_applicants import update_booster_applicants_fields
from database.orders_dungeon import check_order_full, get_order_info
from utils.embed_order import order_created_embed
from utils.get_message import get_message

import settings

class OrderStaffDungeonView(discord.ui.View):
    @discord.ui.button(label='Tank full', emoji='<:tank:1270969225871360010>', style=discord.ButtonStyle.grey)
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        thread_message = self.thread_message
        thread_view = self.thread_view
        user_id = interaction.user.id
        role = 'tank'
        
        button = thread_view.children[0]
        button.disabled = True

        booster_message = await get_message(self.bot, thread_message, thread_message)
        embed = booster_message.embeds[0]

        update_booster_applicants_fields(embed, role)

        await booster_message.edit(embed=embed, attachments=[], view=self.thread_view)

    @discord.ui.button(label='Healer full', emoji='<:Heal:1082086361936449627>', style=discord.ButtonStyle.grey)
    async def healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        thread_message = self.thread_message
        thread_view = self.thread_view
        user_id = interaction.user.id
        role = 'healer'
        
        button = thread_view.children[1]
        button.disabled = True

        booster_message = await get_message(self.bot, thread_message, thread_message)
        embed = booster_message.embeds[0]

        update_booster_applicants_fields(embed, role)

        await booster_message.edit(embed=embed, attachments=[], view=self.thread_view)
        

    @discord.ui.button(label='Dps full', emoji='<:dps:1257157322044608684>', style=discord.ButtonStyle.grey)
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        thread_message = self.thread_message
        thread_view = self.thread_view
        user_id = interaction.user.id
        role = 'dps'

        button = thread_view.children[2]
        button.disabled = True

        booster_message = await get_message(self.bot, thread_message, thread_message)
        embed = booster_message.embeds[0]

        update_booster_applicants_fields(embed, role)

        await booster_message.edit(embed=embed, attachments=[], view=self.thread_view)
            

    @discord.ui.button(label='Complete Selection', emoji='✅', style=discord.ButtonStyle.success, row=1)
    async def team(self, interaction: discord.Interaction, button: discord.ui.Button):
        order_started_channel = self.bot.get_channel(settings.ORDER_STARTED_ID)
        boosters = check_order_full(self.order_id)

        # Con esto accedemos a los mensajes del los Staff y de los Boosters
        staff_message = await get_message(self.bot, self.message_id)
        booster_message = await get_message(self.bot, self.thread_message, self.thread_message)

        if boosters:
            await interaction.response.send_message('Selección terminada.', ephemeral=True, delete_after=5)
            
            # Esto es para borrar los botones de ambos mensajes
            self.clear_items()
            self.thread_view.clear_items()
            await staff_message.edit(view=self)
            await booster_message.edit(view=self.thread_view)

            
            thread = await order_started_channel.create_thread(name=f'Order - {self.order_id}', reason='Orden Iniciada', invitable=False)
            order_info = get_order_info(self.order_id)
            tags = f'<@{order_info[17]}><@&{settings.ROLE_SERVER_STAFF_ID}>\n'

            for i, booster_id in enumerate(boosters):
                tags += f'<@{booster_id}>'
                booster_dm = await self.bot.fetch_user(booster_id)
                await booster_dm.send(f'¡La orden `{self.order_name}` empezará pronto!\nIngresa en {thread.mention} para recibir más información.')

            embed = order_created_embed(order_info, boosters)

            await thread.send(f'{tags}', embed=embed)
            return
        
        await interaction.response.send_message('La orden no está completa', ephemeral=True)
