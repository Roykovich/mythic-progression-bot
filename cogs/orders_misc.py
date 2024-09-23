import math
import discord
import typing
import requests
from discord.ext import commands
from discord import app_commands

from utils.load_region_servers import realms_autocomplete
from utils.load_spec_and_class import classes_and_spec_autocomplete
from utils.role_tagger import give_all_booster_roles
from utils.load_orders_autocomplete import orders_misc_autocomplete
from utils.get_message import get_message
from utils.embed_order import misc_order_embed, staff_order_misc_embed

from database.orders_misc import create_misc_order, accept_misc_applicant_to_order
from database.orders_misc_applicants import update_accepted_applicants_fields_misc
from views.orders_misc_booster import OrderMiscView
from views.orders_misc_staff import OrderStaffMiscView

import settings


class MiscOrders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='order_misc', description='Crea una orden de miscelaneos')
    @app_commands.describe(order_name='Nombre de la orden')
    @app_commands.describe(order_id='ID de la orden')
    @app_commands.choices(service_type=[
        app_commands.Choice(name='Leveling', value='leveling'),
        app_commands.Choice(name='Achievements', value='achievements'),
        app_commands.Choice(name='Wow era', value='era'),
        app_commands.Choice(name='Harcore', value='harcore'),
        app_commands.Choice(name='Season of Discovery', value='sod'),
        app_commands.Choice(name='Cataclysm', value='cataclysm')
    ])
    @app_commands.describe(description='Descripción de la orden')
    @app_commands.describe(custom_name='Nombre del pj')
    @app_commands.describe(battletag='Battletag')
    @app_commands.choices(payment=[
        app_commands.Choice(name='Gold', value='gold'),
        app_commands.Choice(name='USD', value='usd')
    ])
    @app_commands.describe(amount='Cantidad de pago')
    @app_commands.describe(players='Cantidad de players necesitados (1 - 15)')
    @app_commands.choices(region=[
        app_commands.Choice(name='US', value="US")
    ])
    @app_commands.choices(boostmode=[
        app_commands.Choice(name='Self-Play', value='Self-Play'),
        app_commands.Choice(name='Piloted', value='Piloted')
    ])
    @app_commands.choices(streaming=[
        app_commands.Choice(name='Si', value=0),
        app_commands.Choice(name='No', value=1)
    ])
    @app_commands.autocomplete(class_and_spec=classes_and_spec_autocomplete)
    @app_commands.choices(faccion=[
        app_commands.Choice(name='Alianza', value='ally'),
        app_commands.Choice(name='Horda', value='horde')
    ])
    @app_commands.autocomplete(realm=realms_autocomplete)
    async def misc_order(
        self,
        interaction: discord.Interaction,
        order_name: str,
        order_id: int,
        service_type: app_commands.Choice[str],
        description: typing.Optional[str],
        custom_name: typing.Optional[str],
        battletag: typing.Optional[str],
        payment: app_commands.Choice[str],
        amount: str,
        players: app_commands.Range[int, 1, 15],
        region: app_commands.Choice[str],
        boostmode: app_commands.Choice[str],
        streaming: app_commands.Choice[int],
        class_and_spec: str,
        faccion: app_commands.Choice[str],
        realm: str,
    ):
        orders_channel = self.bot.get_channel(settings.ORDER_CHANNEL_ID)
        await interaction.response.defer()
        
        # Si ninguna descripcion es indicada ocurre esto
        if not description:
            description = 'No description provided'

        if not custom_name:
            custom_name = 'N/A'

        if not battletag:
            battletag = 'N/A'

        # archivo de la imagen para enviarla al thumbnail
        file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        booster_thread_embed = misc_order_embed(order={
            'region': region.value,
            'order_name': order_name,
            'description': description,
            'amount': amount,
            'type': service_type.name,
            'boostmode': boostmode.name,
            'players': players,
            'streaming': streaming.name,
            'class_and_spec': class_and_spec,
            'faccion': faccion.value,
            'realm': realm,
            'payment': payment.value
        })

        booster_thread_view = OrderMiscView(timeout=None)

        booster_thread = await orders_channel.create_thread(
            name=f'{order_name}',
            file=file,
            embed=booster_thread_embed,
            content=f'{give_all_booster_roles()}', 
            view=booster_thread_view
        )

        staff_file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        staff_embed = staff_order_misc_embed(order={
            'region': region.value,
            'order_name': order_name,
            'order_id': order_id,
            'description': description,
            'amount': amount,
            'type': service_type.name,
            'boostmode': boostmode.name,
            'players': players,
            'streaming': streaming.name,
            'class_and_spec': class_and_spec,
            'faccion': faccion.value,
            'realm': realm,
            'payment': payment.value
        })

        staff_view = OrderStaffMiscView(timeout=None)
        staff_order_message = await interaction.followup.send(
            content=f'Orden creada correctamente en {booster_thread.thread.mention}',
            file=staff_file,
            embed=staff_embed,
            view=staff_view,
            wait=True
        )

        # Agregar los datos de la orden a la vista
        staff_view.order_id = order_id
        staff_view.order_name = order_name
        staff_view.thread_message = booster_thread.message.id
        staff_view.thread_view = booster_thread_view
        staff_view.message_id = staff_order_message.id
        staff_view.bot = self.bot

        # creamos la orden
        create_misc_order({
            'order_id': order_id,
            'message_id': staff_order_message.id,
            'thread_id': booster_thread.message.id,
            'creator_id': interaction.user.id,
            'order_name': order_name,
            'description': description,
            'amount': amount,
            'payment': payment.value,
            'boostmode': boostmode.name,
            'region': region.value,
            'type': service_type.name,
            'players': players,
            'streaming': streaming.value,
            'class_and_spec': class_and_spec,
            'faccion': faccion.value,
            'realm': realm,
            'custom_name': custom_name,
            'battletag': battletag
        })

        booster_thread_view.order_id = order_id
        booster_thread_view.message_id = staff_order_message.id
        booster_thread_view.thread_message = booster_thread.message.id
        booster_thread_view.order_name = order_name
        booster_thread_view.bot = self.bot


    @app_commands.command(name='accept_misc_applicant', description='Acepta a un aplicante de la orden de miscelaneos')
    @app_commands.autocomplete(order_id=orders_misc_autocomplete)
    @app_commands.describe(user='Usuario')
    async def accept_misc_applicant(self,
        interaction: discord.Interaction,
        order_id: str,
        user: discord.User
    ):
        order = await accept_misc_applicant_to_order(order_id, user.id)

        await interaction.response.send_message(f'Aplicante {user.mention} ha sido aceptado correctamente', ephemeral=True)
        booster = await self.bot.fetch_user(user.id)
        await booster.send(f'¡Felicidades, has sido aceptado en la orden `{order_id}`!')

        staff_message = await get_message(self.bot, order[0])
        embed = staff_message.embeds[0]

        update_accepted_applicants_fields_misc(embed, order_id)

        await staff_message.edit(embed=embed, attachments=[])
        

async def setup(bot):
    await bot.add_cog(MiscOrders(bot))