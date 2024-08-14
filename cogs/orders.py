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
from utils.role_tagger import give_all_booster_roles
from views.view_order import OrderView
from views.view_command_order import OrderCommandView

from database.orders import create_order, accept_applicant_to_order
from database.applicants import update_accepted_applicants_fields
from database.booster import get_wallet_by_user_id

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
        # crea el embed de la orden para los boosters
        thread_embed = order_embed(
            region, 
            order_name, 
            description, 
            amount, 
            boostmode, 
            traders, 
            keystone_level, 
            runs, 
            timed, 
            streaming, 
            class_and_spec, 
            faccion.value, 
            realm, 
            payment
        )
        thread_view = OrderView(timeout=None) # Crear la vista de la orden
        # crea el hilo de la orden
        thread = await orders_channel.create_thread(
            name=f'{order_name}', 
            file=file, 
            embed=thread_embed, 
            content=f'{give_all_booster_roles()}', 
            view=thread_view
        )

        # crea el embed de la orden para el staff
        staff_file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        staff_embed = staff_order_embed(
            region, 
            order_name, 
            order_id, 
            description, 
            amount, 
            boostmode, 
            traders, 
            keystone_level, 
            runs, 
            timed, 
            streaming, 
            class_and_spec, 
            faccion.value, 
            realm, 
            payment
        )
         # Crear la vista de la orden
        staff_view = OrderCommandView(timeout=None)
        order_message = await interaction.followup.send(
            content=f'Order creada correctamente en {thread.thread.mention}', 
            file=staff_file, 
            embed=staff_embed, 
            view=staff_view, 
            wait=True
        )
        # await interaction.response.send_message(
        #     content=f'Order creada correctamente en {thread.thread.mention}', 
        #     file=staff_file, 
        #     embed=staff_embed, 
        #     view=staff_view
        # )
        # ! Esto lo utilizamos para obtener el id del mensaje original de la orden
        # order_message = await interaction.original_response()
        
        # Agregar los datos de la orden a la vista
        staff_view.order_id = order_id
        staff_view.order_name = order_name
        staff_view.thread_message = thread.message.id
        staff_view.thread_view = thread_view
        staff_view.message_id = order_message.id
        staff_view.bot = self.bot

        print(order_id)
        # Creamos la orden
        create_order(
            order_id, 
            order_message.id, 
            thread.message.id, 
            interaction.user.id, 
            order_name, 
            description, 
            amount, 
            payment.value, 
            boostmode.value, 
            region.value, 
            traders.value, 
            keystone_level, 
            runs, 
            timed.value, 
            streaming.value, 
            class_and_spec, 
            faccion.value, 
            realm, 
            custom_name, 
            battletag
        )
        
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

        # hay que ver con lo delos permisos
        # if interaction: 
        #     await interaction.response.send_message(f'No tienes permisos para crear una orden', ephemeral=True)
        
        # TODO cambiar el ID del usuario de Miguel a id de server staff
        await orders_channel.send(f'<@{settings.ROLE_SERVER_STAFF_ID}> El usuario {interaction.user.mention} ha intentado crear una orden pero ha ocurrido un error: {error_message}')

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
        order = accept_applicant_to_order(order_id, user.id, role.value)
        await interaction.response.send_message(f'Aplicante aceptado correctamente', ephemeral=True)
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

        update_accepted_applicants_fields(
            embed, 
            user.id, 
            raiderio, 
            role.value
        )

        await staff_message.edit(embed=embed, attachments=[])


    @app_commands.command(name='pay_boosters', description='Acredita a los Boosters')
    @app_commands.autocomplete(order_id=orders_autocomplete)
    @app_commands.describe(booster1='Usuario')
    @app_commands.describe(booster2='Usuario')
    @app_commands.describe(booster3='Usuario')
    @app_commands.describe(booster4='Usuario')
    @app_commands.describe(booster5='Usuario')
    @app_commands.describe(booster6='Usuario')
    @app_commands.describe(booster7='Usuario')
    @app_commands.describe(booster8='Usuario')
    @app_commands.describe(booster9='Usuario')
    @app_commands.describe(booster10='Usuario')
    @app_commands.describe(amount='Cantidad a pagar')
    async def pay_booster(self,
        interaction: discord.Interaction,
        order_id: str,
        booster1: discord.User,
        booster2: typing.Optional[discord.User],
        booster3: typing.Optional[discord.User],
        booster4: typing.Optional[discord.User],
        booster5: typing.Optional[discord.User],
        booster6: typing.Optional[discord.User],
        booster7: typing.Optional[discord.User],
        booster8: typing.Optional[discord.User],
        booster9: typing.Optional[discord.User],
        booster10: typing.Optional[discord.User],
        amount: float
    ):
        await interaction.response.defer()
        boosters = [booster1, booster2, booster3, booster4, booster5, booster6, booster7, booster8, booster9, booster10]

        get_wallets = await get_wallet_by_user_id(boosters)
        print(f'[+] Wallets: {get_wallets}')

        if len(get_wallets) < 1:
            await interaction.followup.send(f'No se encontraron wallets para los boosters indicados')
            return

        transactions = []
        guild = await self.bot.fetch_guild(settings.GUILD_ID.id)

        # Agregar una busqueda de la id del creador de la orden para colocarlo en payment_method

        for wallet_id in get_wallets:
            data = {
                'amount': amount,
                'action': 'credit',
                'transaction_detail': f'Order-{order_id}',
                'consumer_key': settings.WP_SWINGS_CLIENT,
                'consumer_secret': settings.WP_SWINGS_SECRET,
                'payment_method': 'Acreditado por supplier'
            }
            headers = {
                'Content-Type': 'application/json'
            }           
            response = requests.put(url=f'https://mythicprogression.com/wp-json/wsfw-route/v1/wallet/{wallet_id[0]}', json=data, headers=headers)
            json = response.json()
            # ! Ver si podemos utilizar las transactions_id en el mensaje del comando
            if json['response'] == 'success':
                print(f'[+] Transaction {json['response']}\t| Balance: {json['balance']}\t\t| ID: {json['transaction_id']}')
                transactions.append({
                    'id': json['transaction_id'],
                    'booster': await guild.fetch_member(wallet_id[1]),
                })

        codeblock = '```ansi\n'

        for transaction in transactions:
            codeblock += f'[2;33m[2;34m[?][0m[2;33m[0m Booster: [2;36m{transaction['booster'].nick if transaction['booster'].nick is not None else transaction['booster'].global_name}[0m\n[2;34m[2;31m[!][0m[2;34m[0m Transaction ID: [2;36m{transaction['id']}[0m\n[2;31m[2;32m[+][0m[2;31m[0m Amount: $[2;36m{amount}[0m\n\n'
        
        codeblock += '\n```'

        # Agregar un logger para guardar los pagos realizados
        await interaction.followup.send(f'Boosters pagados correctamente:\n{codeblock}')

async def setup(bot):
    await bot.add_cog(Orders(bot))