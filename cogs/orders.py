import discord
import typing
import requests
from discord.ext import commands
from discord import app_commands

from utils.load_region_servers import realms_autocomplete
from utils.load_spec_and_class import classes_and_spec_autocomplete
from utils.load_orders_autocomplete import orders_autocomplete
from utils.embed_order import order_embed
from utils.embed_order import staff_order_embed
from views.view_order import OrderView
from views.view_command_order import OrderCommandView

from database.orders import create_order, accept_applicant_to_order
from database.applicants import update_accepted_applicants_fields

from utils.get_message import get_message

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
    @app_commands.describe(custom_name='Nombre del pj')
    @app_commands.describe(battletag='Battletag')
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
        custom_name: typing.Optional[str],
        battletag: typing.Optional[str],
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
        orders_channel = self.bot.get_channel(settings.ORDER_CHANNEL_ID)

        # Si ninguna descripcion es indicada ocurre esto
        if not description:
            description = 'No description provided'

        if not custom_name:
            custom_name = 'N/A'

        if not battletag:
            battletag = 'N/A'

        # archivo de la imagen para enviarla al thumbnail
        file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        # crea el embed de la orden para los boosters
        thread_embed = order_embed(region, order_name, description, amount, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion.value, realm, payment)
        thread_view = OrderView(timeout=None) # Crear la vista de la orden
        # crea el hilo de la orden
        # ? Donde dice CAMBIAR ESTO DE AQUÍ, se debe de cambiar por el mensaje que se quiere enviar al hilo, en este caso el tag a los boosters
        thread = await orders_channel.create_thread(name=f'{order_name}', file=file, embed=thread_embed, content=f'CAMBIAR ESTO DE AQUÍ', view=thread_view)

        # crea el embed de la orden para el staff
        staff_file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        staff_embed = staff_order_embed(region, order_name, order_id, description, amount, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion.value, realm, payment)
        staff_view = OrderCommandView(timeout=None) # Crear la vista de la orden
        await interaction.response.send_message(content=f'Order creada correctamente en {thread.thread.mention}', file=staff_file, embed=staff_embed, view=staff_view)
        # Esto lo utilizamos para obtener el id del mensaje original de la orden
        order_message = await interaction.original_response()
        staff_view.order_id = order_id
        staff_view.order_name = order_name
        staff_view.thread_message = thread.message.id
        staff_view.thread_view = thread_view
        staff_view.message_id = order_message.id
        staff_view.bot = self.bot

        # Creamos la orden
        create_order(order_id, order_message.id, thread.message.id, interaction.user.id, order_name, description, amount, payment.value, boostmode.value, region.value, traders.value, keystone_level, runs, timed.value, streaming.value, class_and_spec, faccion.value, realm, custom_name, battletag)
        
        thread_view.order_id = order_id
        thread_view.message_id = order_message.id
        thread_view.thread_message = thread.message.id
        thread_view.order_name = order_name
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

    @app_commands.command(name='accept_applicant', description='Acepta un aplicante')
    @app_commands.autocomplete(order_id=orders_autocomplete)
    @app_commands.describe(user='Usuario')
    @app_commands.choices(role=[
        app_commands.Choice(name='tank', value='tank'),
        app_commands.Choice(name='healer', value='healer'),
        app_commands.Choice(name='first dps', value='first_dps'),
        app_commands.Choice(name='second dps', value='second_dps')
    ])
    async def accept_applicant(self,
        interaction: discord.Interaction,
        order_id: str,
        user: discord.User,
        role: app_commands.Choice[str],
        ):
        print(user.id)
        order = accept_applicant_to_order(order_id, user.id, role.value)
        await interaction.response.send_message(f'Aplicante aceptado correctamente', ephemeral=True)
        print(order)
        if role.value == 'tank':
            raiderio = order[6]
        elif role.value == 'healer':
            raiderio = order[8]
        elif role.value == 'first_dps':
            raiderio = order[10]
        else:
            raiderio = order[12]

        staff_message = await get_message(self.bot, order[2])
        embed = staff_message.embeds[0]

        update_accepted_applicants_fields(embed, user.id, raiderio, role.value)

        await staff_message.edit(embed=embed, attachments=[])


    @app_commands.command(name='pay_boosters', description='Acredita a los Boosters')
    @app_commands.autocomplete(order_id=orders_autocomplete)
    @app_commands.describe(booster1='Usuario')
    @app_commands.describe(booster2='Usuario')
    @app_commands.describe(booster3='Usuario')
    @app_commands.describe(booster4='Usuario')
    async def pay_booster(self,
        interaction: discord.Interaction,
        order_id: str,
        booster1: typing.Optional[discord.User],
        booster2: typing.Optional[discord.User],
        booster3: typing.Optional[discord.User],
        booster4: typing.Optional[discord.User]
    ):
        ...
        # await interaction.response.send_message(f'Boosters acreditados correctamente', ephemeral=True)
        # boosters = [26, 27, 59, 75]

        # for booster in boosters:
        #     response = requests.get(f'https://mythicprogression.com/wp-json/wsfw-route/v1/wallet/{booster}?consumer_key={settings.WP_SWINGS_CLIENT}&consumer_secret={settings.WP_SWINGS_SECRET}').json()
        #     print(response)

        # for booster in boosters:
        #     data = {
        #         'amount': 5,
        #         'action': 'credit',
        #         'transaction_detail': 'Pago por boosteo (?)',
        #         'consumer_key': settings.WP_SWINGS_CLIENT,
        #         'consumer_secret': settings.WP_SWINGS_SECRET,
        #         'payment_method': 'Petro'
        #     }
        #     headers = {
        #         'Content-Type': 'application/json'
        #     }           
        #     response = requests.put(url=f'https://mythicprogression.com/wp-json/wsfw-route/v1/wallet/{booster}', json=data, headers=headers)
        #     json = response.json()
        #     print(json)



async def setup(bot):
    await bot.add_cog(Orders(bot))