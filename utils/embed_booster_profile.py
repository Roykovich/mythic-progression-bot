import discord
from utils.raiderio import get_raiderio_profile, get_lowest_ilvl

icons = {
    'horde': '<:Horde:1136423725152084068>',
    'alliance': '<:Ally:1136423791799586909>',
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
    'Death Knight': '<:dk:1082090829138645064>',
    'TANK': '<:tank:1270969225871360010>',
    'HEALING': '<:Heal:1082086361936449627>',
    'DPS': '<:dps:1257157322044608684> ',
}

booster_colours = {
    'Booster': 0x1bf30b,
    'Gold Booster': 0xefc714,
    'Veteran Booster': 0x6045c9,
    'Elite Booster': 0x9f05b1,
    'Master Booster': 0xe58122
}

async def embed_booster_profile(booster, booster_points, booster_rank, characters):
    basic_info = ''
    pve_info = ''
    ilvl_info = ''
    
    for character in characters:
        pj = get_raiderio_profile(character[9], character[2].replace(" ", "%20"), character[1])
        lowest_ilvl = get_lowest_ilvl(pj['gear']['items'])
        basic_info += f'{icons[character[3]]} {character[3]}\n{icons[character[5]]} **__{character[1]}__**\n{icons[character[4]]} {character[2]}\n\n'
        pve_info += f'{icons['DPS']} {character[6]}\n{ icons['TANK']} {character[7]}\n{icons['HEALING']} {character[8]}\n\n'
        ilvl_info += f'<:bags:1107428757884637184> {pj["gear"]["item_level_equipped"]} ({lowest_ilvl})\n\n\n\n'

    embed = discord.Embed(
        title=f'{booster.display_name} profile',
        color=booster_colours[booster_rank],
        description=f'No se que agregar aca aiuda :c',
    )

    embed.set_thumbnail(url=booster.avatar.url)
    embed.add_field(name=f'Booster Rank', value=f'<:pts:1172085820191154206> {booster_rank}', inline=True)
    embed.add_field(name='Points', value=f'<a:clap:1237923945068499036> {booster_points}', inline=True)
    embed.add_field(name='', value='', inline=True)
    embed.add_field(name='Basic info', value=basic_info, inline=True)
    embed.add_field(name='Raiderio', value=pve_info, inline=True)
    embed.add_field(name='Ilvl Info', value=ilvl_info, inline=True)
    

    return embed