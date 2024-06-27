import discord
import requests
import typing
from discord.ext import commands
from discord import app_commands

from utils.load_region_servers import realms_autocomplete
from utils.load_spec_and_class import classes_and_spec_autocomplete
from utils.embed_order import order_embed
from utils.embed_order import staff_order_embed

import settings

class Orders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='orden', description='Crea una orden')
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
        print(order_name, payment, amount, region, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm)
        
        orders_channel = self.bot.get_channel(settings.ORDER_CHANNEL_ID)

        if not description:
            description = 'No description provided'

        file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        embed = order_embed(region, order_name, description, amount, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm, payment)
        staff_embed = staff_order_embed(region, order_name, order_id, description, amount, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm, payment)

        thread = await orders_channel.create_thread(name=f'{order_name}', file=file, embed=embed, content=f'<@&1252403838888185899>')
        staff_file = discord.File('images/logo_mp.png', filename='logo_mp.png')
        order_message = await interaction.response.send_message(content=f'Order creada correctamente en {thread.thread.mention}', file=staff_file, embed=staff_embed)

    @orderslash.error
    async def orderslash_error(self, interaction: discord.Interaction, error):
        orders_channel = self.bot.get_channel(settings.COMMAND_CHANNEL_ID)
        # TODO cambiar el ID del usuario de Miguel a id de server staff
        await interaction.response.send_message(f'No tienes permisos para crear una orden', ephemeral=True)
        await orders_channel.send(f'<@443948776562884620> El usuario {interaction.user.mention} ha intentado crear una orden pero ha ocurrido un error: {error}')

async def setup(bot):
    await bot.add_cog(Orders(bot))