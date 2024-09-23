import math
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
from views.view_staff_dungeon_order import OrderStaffDungeonView

from database.orders_dungeon import create_order, accept_applicant_to_order
from database.orders_dungeon_applicants import update_accepted_applicants_fields
from database.booster import get_wallet_by_user_id

from utils.get_message import get_message

import settings

roles = {
    'tank': '<:tank:1270969225871360010>',
    'healer': '<:Heal:1082086361936449627>',
    'first_dps': '<:dps:1257157322044608684>',
    'second_dps': '<:dps:1257157322044608684>'
}

class DungeonOrders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='order_dungeon', description='Crea una orden de mazmorras')
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
        staff_view = OrderStaffDungeonView(timeout=None)
        order_message = await interaction.followup.send(
            content=f'Order creada correctamente en {thread.thread.mention}', 
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

        # Creamos la orden haciendo la query a la database
        create_order({
            'order_id': order_id, 
            'message_id': order_message.id, 
            'thread_id': thread.message.id, 
            'creator_id': interaction.user.id, 
            'order_name': order_name, 
            'description': description, 
            'amount': amount, 
            'payment': payment.value, 
            'boostmode': boostmode.value, 
            'region': region.value, 
            'traders': traders.value, 
            'keystone_level': keystone_level, 
            'runs': runs, 
            'timed': timed.value, 
            'streaming': streaming.value, 
            'class_and_spec': class_and_spec, 
            'faccion': faccion.value, 
            'realm': realm, 
            'custom_name': custom_name, 
            'battletag': battletag
        })
        
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
        
        await orders_channel.send(f'<@&{settings.ROLE_SERVER_STAFF_ID}> El usuario {interaction.user.mention} ha intentado crear una orden pero ha ocurrido un error: {error_message}')

    @app_commands.command(name='accept_dungeon_applicant', description='Acepta un aplicante')
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
        
        await interaction.response.send_message(f'Aplicante <@{user.id}> aceptado correctamente', ephemeral=True)
        booster = await self.bot.fetch_user(user.id)
        await booster.send(f'¡Felicidades, has sido aceptado en la orden `{order_id}` como {roles[role.value]}{role.value}!')

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
    @app_commands.describe(dollars='Dolares a pagar')
    @app_commands.describe(cents='Centavos a pagar. [Si es 12.3 coloca 12 y 30 || Si es 12.03 coloca 12 y 3]')
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
        dollars: app_commands.Range[int, 0, 200],
        cents: app_commands.Range[int, 0, 99],
    ):
        await interaction.response.defer()
        # Guardamos a los Boosters en una lista para luego loopear en ella a la hora de realizar los pagos
        boosters = [booster1, booster2, booster3, booster4, booster5, booster6, booster7, booster8, booster9, booster10]
        # Guardamos la cantidad correcta a pagar
        new_amount = float(f'{dollars}.{cents if cents > 9 else f"0{cents}"}') 
        # Accreditor
        accreditor = interaction.user.nick if interaction.user.nick is not None else interaction.user.global_name

        # Si el monto a pagar es mayor a 200 se redondea a 200
        # Ya que la unica forma de que pase de 200 es que se pase de 0.1 centavos hacia 0.99
        if new_amount > 200:
            new_amount = float(math.floor(new_amount))
            await interaction.followup.send(f'El monto máximo a pagar es de `$200`', ephemeral=True)

        get_wallets = await get_wallet_by_user_id(boosters)
        print(f'[+] Wallets: {get_wallets}')

        if len(get_wallets) < 1:
            await interaction.followup.send(f'No se encontraron wallets para los boosters indicados')
            return

        transactions = []
        guild = await self.bot.fetch_guild(settings.GUILD_ID.id)

        for wallet_id in get_wallets:
            data = {
                'amount': new_amount,
                'action': 'credit',
                'transaction_detail': f'Order-{order_id}',
                'consumer_key': settings.WP_SWINGS_CLIENT,
                'consumer_secret': settings.WP_SWINGS_SECRET,
                'payment_method': f'Acreditado por {accreditor}'
            }
            headers = {
                'Content-Type': 'application/json'
            }           
            response = requests.put(
                url=f'https://mythicprogression.com/wp-json/wsfw-route/v1/wallet/{wallet_id[0]}', 
                json=data, 
                headers=headers
            ).json()

            if response['response'] == 'success':
                print(f'[+] Transaction {response['response']}\t| Balance: {response['balance']}\t\t| ID: {response['transaction_id']}')
                transactions.append({
                    'id': response['transaction_id'],
                    'booster': await guild.fetch_member(wallet_id[1]),
                })

        codeblock = '```ansi\n'

        for transaction in transactions:
            codeblock += f'[2;33m[2;34m[?][0m[2;33m[0m Booster: [2;36m{transaction['booster'].nick if transaction['booster'].nick is not None else transaction['booster'].global_name}[0m\n[2;34m[2;31m[!][0m[2;34m[0m Transaction ID: [2;36m{transaction['id']}[0m\n[2;31m[2;32m[+][0m[2;31m[0m Amount: $[2;36m{new_amount}[0m\n\n'
        
        codeblock += '\n```'

        # Agregar un logger para guardar los pagos realizados
        await interaction.followup.send(f'Boosters pagados correctamente:\n{codeblock}')

async def setup(bot):
    await bot.add_cog(DungeonOrders(bot))