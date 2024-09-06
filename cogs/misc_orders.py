import math
import discord
import typing
import requests
from discord.ext import commands
from discord import app_commands

from utils.load_region_servers import realms_autocomplete
from utils.load_spec_and_class import classes_and_spec_autocomplete
from utils.role_tagger import give_all_booster_roles
from utils.load_orders_autocomplete import orders_autocomplete
from utils.get_message import get_message

import settings


class MiscOrders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='order_misc', description='Crea una orden de miscelaneos')
    @app_commands.describe(order_name='Nombre de la orden')
    @app_commands.describe(order_id='ID de la orden')
    @app_commands.choices(service_type=[
        app_commands.Choice(name='leveling', value='leveling'),
        app_commands.Choice(name='achievements', value='achievements'),
        app_commands.Choice(name='wow era', value='era'),
        app_commands.Choice(name='harcore', value='harcore'),
        app_commands.Choice(name='season of discovery', value='sod'),
        app_commands.Choice(name='cataclysm', value='cataclysm')
    ])
    @app_commands.describe(description='Descripción de la orden')
    @app_commands.describe(custom_name='Nombre del pj')
    @app_commands.describe(battletag='Battletag')
    @app_commands.choices(payment=[
        app_commands.Choice(name='Gold', value='gold'),
        app_commands.Choice(name='USD', value='usd')
    ])
    @app_commands.describe(amount='Cantidad de pago')
    @app_commands.describe(players='Cantidad de players necesitados')
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
        service_type: str,
        description: typing.Optional[str],
        custom_name: typing.Optional[str],
        battletag: typing.Optional[str],
        payment: app_commands.Choice[str],
        amount: str,
        players: int,
        region: app_commands.Choice[str],
        boostmode: app_commands.Choice[str],
        streaming: app_commands.Choice[int],
        class_and_spec: str,
        faccion: app_commands.Choice[str],
        realm: str,
    ):
        return
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
            'region': region,
            'order_name': order_name,
            'description': description,
            'amount': amount,
            'type': service_type,
            'boostmode': boostmode,
            'players': players,
            'streaming': streaming,
            'class_and_spec': class_and_spec,
            'faccion': faccion,
            'realm': realm,
            'payment': payment
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
            'region': region,
            'order_name': order_name,
            'order_id': order_id,
            'description': description,
            'amount': amount,
            'type': service_type,
            'boostmode': boostmode,
            'players': players,
            'streaming': streaming,
            'class_and_spec': class_and_spec,
            'faccion': faccion,
            'realm': realm,
            'payment': payment
        })

        staff_view = StaffOrderMiscView(timeout=None)
        staff_order_message = await interaction.followup.send(
            content=f'Orden creada correctamente en {booster_thread.mention}',
            file=staff_file,
            embed=staff_embed,
            view=staff_view,
            wait=True
        )

        # Agregar los datos de la orden a la vista
        staff_view.order_id = order_id
        staff_view.order_name = order_name
        staff_view.thread_message = thread.message.id
        staff_view.thread_view = thread_view
        staff_view.message_id = order_message.id
        staff_view.bot = self.bot

        # * Aqui comando de la base de datos para guardar la orden

        booster_thread_view.order_id = order_id
        booster_thread_view.message_id = order_message.id
        booster_thread_view.thread_message = thread.message.id
        booster_thread_view.order_name = order_name
        booster_thread_view.bot = self.bot

        

async def setup(bot):
    await bot.add_cog(MiscOrders(bot))