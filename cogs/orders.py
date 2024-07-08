import discord
import requests
import typing
import uuid
from discord.ext import commands
from discord import app_commands

from utils.load_region_servers import realms_autocomplete
from utils.load_spec_and_class import classes_and_spec_autocomplete
from utils.embed_order import order_embed
from utils.embed_order import staff_order_embed
from views.view_order import OrderView
from views.view_order import get_cursor

import settings

 # TODO:
    # - Agregar que roles queremos taggear a la hora de crear una orden
    # - Agregar un campo para aplicar personajes especificas

class Orders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='order', description='Crea una orden')
    @app_commands.describe(order_name='Nombre de la orden')
    @app_commands.describe(order_id='ID de la orden')
    @app_commands.describe(description='Descripción de la orden')
    @app_commands.choices(payment=[
        app_commands.Choice(name='Gold', value='gold'),
        app_commands.Choice(name='USD', value='usd')
    ])
    @app_commands.describe(amount='Cantidad de pago')
    @app_commands.choices(region=[
        app_commands.Choice(name='US', value="US")
    ])
    @app_commands.choices(boostmode=[
        app_commands.Choice(name='Self-Play', value='Self-Play'),
        app_commands.Choice(name='Piloted', value='Piloted')
    ])
    @app_commands.choices(traders=[
        app_commands.Choice(name='No trader', value=0),
        app_commands.Choice(name='1', value=1),
        app_commands.Choice(name='2', value=2),
        app_commands.Choice(name='3', value=3)
    ])
    @app_commands.describe(keystone_level='Nivel de la piedra')
    @app_commands.describe(runs='Cantidad de runs')
    @app_commands.choices(timed=[
        app_commands.Choice(name='Timed', value=0),
        app_commands.Choice(name='Untimed', value=1),
        app_commands.Choice(name='N/A', value=2)
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
    # @app_commands.checks.has_role(int(settings.ROLE_SERVER_STAFF_ID))
    async def orderslash(self,
        interaction: discord.Interaction,
        order_name: str,
        order_id: str,
        description: typing.Optional[str],
        payment: app_commands.Choice[str],
        amount: str,
        region: app_commands.Choice[str],
        boostmode: app_commands.Choice[str],
        traders: app_commands.Choice[int],
        keystone_level: int,
        runs: int,
        timed: app_commands.Choice[int],
        streaming: app_commands.Choice[int],
        class_and_spec: str,
        faccion: app_commands.Choice[str],
        realm: str,
        ):
        # print(order_name, payment, amount, region, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm)
        
        orders_channel = self.bot.get_channel(settings.ORDER_CHANNEL_ID)

        # Si ninguna descripcion es indicada ocurre esto
        if not description:
            description = 'No description provided'

        # archivo de la imagen para enviarla al thumbnail
        file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        thread_embed = order_embed(region, order_name, description, amount, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm, payment)
        thread_view = OrderView(timeout=None)
        thread = await orders_channel.create_thread(name=f'{order_name}', file=file, embed=thread_embed, content=f'CAMBIAR ESTO DE AQUÍ', view=thread_view)

        staff_embed = staff_order_embed(region, order_name, order_id, description, amount, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm, payment)
        staff_file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        await interaction.response.send_message(content=f'Order creada correctamente en {thread.thread.mention}', file=staff_file, embed=staff_embed)
        order_message = await interaction.original_response()

        db = get_cursor()
        new_order_id = uuid.uuid4()
        db.execute('INSERT INTO orders (id, order_id, message_id, thread_id) VALUES (?, ?, ?, ?)', (new_order_id, order_id, order_message.id, thread.message.id))
        thread_view.order_id = order_id
        thread_view.message_id = order_message.id
        thread_view.bot = self.bot

    @orderslash.error
    async def orderslash_error(self, interaction: discord.Interaction, error):
        orders_channel = self.bot.get_channel(settings.COMMAND_CHANNEL_ID)
        error_message = ''
        if hasattr(error, 'message'):
            error_message = error.message
            print(error_message)
        else:
            error_message = error
            print(error)

        # TODO cambiar el ID del usuario de Miguel a id de server staff
        await interaction.response.send_message(f'No tienes permisos para crear una orden', ephemeral=True)
        await orders_channel.send(f'<@443948776562884620> El usuario {interaction.user.mention} ha intentado crear una orden pero ha ocurrido un error: {error_message}')

    @commands.command(name='accept applicant', description='Acepta un aplicante')
    @app_commands.describe(order_id='ID de la orden')
    @app_commands.describe(user_id='ID del usuario')
    @app_commands.choices(role=[
        app_commands.Choice(name='tank', value='tank'),
        app_commands.Choice(name='healer', value='healer'),
        app_commands.Choice(name='dps', value='dps')
    ])
    async def accept_applicant(self,
        interaction: discord.Interaction,
        order_id: str,
        user_id: str,
        faccion: app_commands.Choice[str],
        ):
        ...



async def setup(bot):
    await bot.add_cog(Orders(bot))