import discord
from database.applicants import get_applications

icons = {
    'horde': '<:Horde:1136423725152084068>',
    'ally': '<:Ally:1136423791799586909>',
    'Mage': '<:Mage:1082090834725449839>',
    'Paladin': '<:Paladin:1082090835845328966>',
    'Hunter': '<:Hunter:1082090832699588628>',
    'Evoker': '<:Evoke:1082090830975729825>',
    'Rogue': '<:Rogue:1082090930103922800>',
    'Priest': '<:Priest:1082098529352294420>',
    'Warrior': '<:Warrior:1082090838978478120>',
    'Demon Hunter': '<:classicon_demonhunter:1082090824201941043>',
    'Druid': '<:classicon_druid:1082090825942577192>',
    'Shaman': '<:classicon_shaman:1082090828161351751>',
    'Monk': '<:classicon_monk:1082090827108581417>',
    'Warlock': '<:Warlock:1082090950765060137>',
    'Death Knight': '<:dk:1082090829138645064>'
}

def faction_choice(faction):
    return icons['horde'] if faction.value == 'horde' else icons['ally']

def class_choice(class_name):
    name = class_name.split(' -> ')[0]
    return icons[name]

# TODO change this to a dynamic value
def order_embed(region, order_name, description, amount, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm, payment):
    embed = discord.Embed(
        title=f'({region.value}) {order_name}',
        description=f'Description: {description}',
        color=discord.Color.green()
    )

    embed.add_field(name='Region', value=region.value.capitalize(), inline=True)
    embed.add_field(name='Play mode', value=boostmode.name, inline=True)
    embed.add_field(name='Traders amount', value=traders.value, inline=True)
    embed.add_field(name='Timed', value=timed.name, inline=True)
    embed.add_field(name='Streaming', value=streaming.name, inline=True)
    embed.add_field(name='Runs quantity', value=runs, inline=True)
    embed.add_field(name='Faction and Realm', value=f'{faction_choice(faction=faccion)} {faccion.value.capitalize()}\n<:quest:1107428715962572862> {realm}', inline=True)
    embed.add_field(name='Class & Specification', value=f'{class_choice(class_and_spec)} {class_and_spec.replace(' -> ', ' - ')}', inline=True)
    embed.add_field(name='Keystone Lvl', value=f'<:Key:1105410551271653487> {keystone_level}+', inline=True)
    embed.add_field(name='<:Tank:1082086003113734214> Tank (0)', value=f'0/1', inline=True)
    embed.add_field(name='<:Heal:1082086361936449627> Healer (0)', value=f'0/1', inline=True)
    embed.add_field(name='<:Dps:1082087375485812747> DPS (0)', value=f'0/2', inline=True)
    embed.set_thumbnail(url='attachment://logo_mp.png')
    embed.set_footer(text=f'Price: {amount} | {'USD' if payment.value == 'usd' else 'Gold'}')

    return embed

# TODO change this to a dynamic value
def staff_order_embed(region, order_name, order_id, description, amount, boostmode, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm, payment):
    embed = discord.Embed(
        title=f'({region.value}) [#{order_id}] {order_name}',
        description=f'Description: {description}',
        color=discord.Color.green()
    )

    embed.add_field(name='Region', value=region.value.capitalize(), inline=True)
    embed.add_field(name='Play mode', value=boostmode.name, inline=True)
    embed.add_field(name='Traders amount', value=traders.value, inline=True)
    embed.add_field(name='Timed', value=timed.name, inline=True)
    embed.add_field(name='Streaming', value=streaming.name, inline=True)
    embed.add_field(name='Runs quantity', value=runs, inline=True)
    embed.add_field(name='Faction and Realm', value=f'{faction_choice(faction=faccion)} {faccion.value.capitalize()}\n<:quest:1107428715962572862> {realm}', inline=True)
    embed.add_field(name='Class & Specification', value=f'{class_choice(class_and_spec)} {class_and_spec.replace(' -> ', ' - ')}', inline=True)
    embed.add_field(name='Keystone Lvl', value=f'<:Key:1105410551271653487> {keystone_level}+', inline=True)
    embed.add_field(name='<:Tank:1082086003113734214> Tank', value='N/A', inline=True)
    embed.add_field(name='<:Heal:1082086361936449627> Healer', value='N/A', inline=True)
    embed.add_field(name='<:dps:1257157322044608684> DPS', value='N/A', inline=True)
    embed.add_field(name='<:Tank:1082086003113734214> Tank picked', value='N/A', inline=True)
    embed.add_field(name='<:Heal:1082086361936449627> Healer picked', value='N/A', inline=True)
    embed.add_field(name='<:dps:1257157322044608684> DPS picked', value='N/A', inline=True)
    embed.set_thumbnail(url='attachment://logo_mp.png')
    embed.set_footer(text=f'Price: {amount} | {'USD' if payment.value == 'usd' else 'Gold'} | order_id: {order_id}')

    return embed