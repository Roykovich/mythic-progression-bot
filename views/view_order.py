import discord
import sqlite3
import uuid
import random # ! Esto es solo para emular el valor del raiderio

import settings

COMMAND_CHANNEL_ID = settings.COMMAND_CHANNEL_ID

sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)
sqlite3.register_converter("GUID", lambda b: uuid.UUID(bytes_le=b))

connection = sqlite3.connect('mythic.db', isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)
db = connection.cursor()

db.execute('CREATE TABLE IF NOT EXISTS orders (id GUID PRIMARY KEY, order_id TEXT, message_id INTEGER, thread_id INTEGER)')
db.execute('CREATE TABLE IF NOT EXISTS applications (id GUID PRIMARY KEY, order_id TEXT, message_id INTEGER, user_id INTEGER, role TEXT, raiderio INTEGER)')

def get_cursor():
    return db

def apply(order_id, message_id, user_id, role, raiderio):
    new_order_id = uuid.uuid4()
    db.execute('INSERT INTO applications (id, order_id, message_id, user_id, role, raiderio) VALUES (?, ?, ?, ?, ?, ?)', (new_order_id, order_id, message_id, user_id, role, raiderio))

def cancel_application(order_id, user_id):
    result = db.execute('DELETE FROM applications WHERE order_id = ? AND user_id = ?', (order_id, user_id)).rowcount

    return result

def update_after_cancel(embed, order_id, role):
    applications = get_applications(order_id, role)
    update_applicants_fields(embed, applications, role)

def get_applications(order_id, role):
    # TODO Recordar agregar a la tabla las cosas como el nombre de usuario y el raiderio
    applications =  db.execute('SELECT user_id, raiderio FROM applications WHERE order_id = ? AND role = ?', (order_id, role.lower())).fetchall()

    return applications

def io_colour_checker(io):
    colours = {
        1000: "⚪",
        1200: "🟢",
        2200: "🔵",
        2500: "🟣",
        2900: "🟡",
        3000: "🟤",
        3500: "🟠",
    }

    if io <= 0:
        return '❌' 
    elif io <= 1000:
        return colours[1000]
    elif io <= 2200:
        return colours[1200]
    elif io <= 2500:
        return colours[2200]
    elif io <= 2900:
        return colours[2500]
    elif io <= 3000:
        return colours[2900]
    elif io <= 3500:
        return colours[3000]
    else:
        return colours[3500]

def display_applicants(applications):
    if len(applications) == 0:
        return 'N/A'

    value = ''
    for application in applications:
        raiderio = application[1]
        value += f'<@{application[0]}> ({io_colour_checker(raiderio)} {raiderio})\n'
    
    return value
    
def check_already_applicated(order_id, user_id, role):
    application = db.execute('SELECT user_id FROM applications WHERE order_id = ? AND user_id = ? AND role = ?', (order_id, user_id, role)).fetchone()

    return application

def update_applicants_fields(embed, applicants, role):
    field = 9 if role == 'tank' else 10 if role == 'healer' else 11
    embed.set_field_at(field, name=embed.fields[field].name, value=display_applicants(applicants), inline=True)
    
async def get_message(bot, message_id):
    channel = bot.get_channel(COMMAND_CHANNEL_ID)
    message = await channel.fetch_message(message_id)

    return message

# TODO cambiar la imagen a URL en imgur o algo
# Ver como se aplica un for para las aplicaciones y ponerlo como un valor dinamico o usarlo directamente del valor del embed y solo agregarlo con un salto de linea
# mover toda la DB a un archivo propio y hacer un archivo de funciones para las DB
# y que cada boton solo llame a estas funciones para que sea mas legible y modular
# Cuando se aplique un boton, se debe de actualizar el embed con los aplicantes (disabled cuando ya se selecciono los roles)
# crear tabla para los aplicantes aceptados con el id de la orden y el id del usuario y su rol

class OrderView(discord.ui.View):
    @discord.ui.button(label='Tank', emoji='<:Tank:1082086003113734214>', style=discord.ButtonStyle.grey)
    async def tank(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'tank'

        if check_already_applicated(order_id, user_id, role):
            # interaction.channel.send(f'Ya aplicaste para este rol.', ephemeral=True, delete_after=5)
            return

        apply(order_id, message_id, user_id, role, random.randint(600, 3500))
        applicants = get_applications(order_id, role)

        staff_message = await get_message(self.bot, message_id)
        embed = staff_message.embeds[0]
        
        update_applicants_fields(embed, applicants, role)
        
        await staff_message.edit(embed=embed, attachments=[])

    @discord.ui.button(label='Healer', emoji='<:Heal:1082086361936449627>', style=discord.ButtonStyle.grey)
    async def healer(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'healer'

        if check_already_applicated(order_id, user_id, role):
            # interaction.channel.send(f'Ya aplicaste para este rol.', ephemeral=True, delete_after=5)
            return

        apply(order_id, message_id, user_id, role, random.randint(600, 2500))
        applicants = get_applications(order_id, role)

        staff_message = await get_message(self.bot, message_id)
        embed = staff_message.embeds[0]
        
        update_applicants_fields(embed, applicants, role)
        
        await staff_message.edit(embed=embed, attachments=[])
        

    @discord.ui.button(label='Dps', emoji='<:dps:1257157322044608684>', style=discord.ButtonStyle.grey)
    async def dps(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        message_id = self.message_id
        user_id = interaction.user.id
        role = 'dps'

        if check_already_applicated(order_id, user_id, role):
            # interaction.channel.send(f'Ya aplicaste para este rol.', ephemeral=True, delete_after=5)
            return

        apply(order_id, message_id, user_id, role, random.randint(600, 2500))
        applicants = get_applications(order_id, role)

        staff_message = await get_message(self.bot, message_id)
        embed = staff_message.embeds[0]
        
        update_applicants_fields(embed, applicants, role)
        
        await staff_message.edit(embed=embed, attachments=[])
            

    @discord.ui.button(label='Team application', emoji='⚔️', style=discord.ButtonStyle.blurple, row=1, disabled=True)
    async def team(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
    
    @discord.ui.button(label='Cancel', emoji='❌', style=discord.ButtonStyle.red, row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        order_id = self.order_id
        user_id = interaction.user.id
        staff_message = await get_message(self.bot, self.message_id)
        embed = staff_message.embeds[0]

        if cancel_application(order_id, user_id) == 0:
            # interaction.channel.send(f'No tienes aplicaciones para cancelar.', ephemeral=True, delete_after=5)
            return
        
        update_after_cancel(embed, order_id, 'tank')
        update_after_cancel(embed, order_id, 'healer')
        update_after_cancel(embed, order_id, 'dps')

        await staff_message.edit(embed=embed, attachments=[])

        
        
        


        


        

