import discord

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
    'Death Knight': '<:dk:1082090829138645064>',
    'tank': '<:tank:1270969225871360010>',
    'healing': '<:Heal:1082086361936449627>',
    'dps': '<:dps:1257157322044608684> ',
}

def raiderio_profile(pj):
    active_role = pj['active_spec_role'].lower()

    embed = discord.Embed(
        title=f'{pj['name']} profile',
        url=f'{pj['profile_url']}',
        color=discord.Color.green(),
        description=f'This char is a {icons[pj['faction']]} {pj['race']} {icons[pj['class']]} **{pj['class']}** __{pj['active_spec_name']}__ ({icons[active_role]} {pj['active_spec_role']}) with `{pj['achievement_points']}` achievement points',
    )

    embed.set_author(name=f'{pj['name']} - {pj['realm']} - {pj['region']} season: [{pj['mythic_plus_scores_by_season'][0]['season']}]')
    embed.set_thumbnail(url=f'{pj['thumbnail_url']}')
    embed.add_field(name='<:bags:1107428757884637184> ilvl', value=pj['gear']['item_level_equipped'], inline=True)
    embed.add_field(name='<:pvp:1136840776698048633> honorable kills', value=pj['honorable_kills'], inline=True)
    embed.add_field(name='<:Key:1105410551271653487> Mythic+ score', value=f'{pj["mythic_plus_scores_by_season"][0]["scores"]["all"]}', inline=True)
    embed.add_field(name='<:tank:1270969225871360010> Tank score', value=f'{pj["mythic_plus_scores_by_season"][0]["scores"]["tank"]}', inline=True)
    embed.add_field(name='<:Heal:1082086361936449627> Healer score', value=f'{pj["mythic_plus_scores_by_season"][0]["scores"]["healer"]}', inline=True)
    embed.add_field(name='<:dps:1257157322044608684> DPS score', value=f'{pj["mythic_plus_scores_by_season"][0]["scores"]["dps"]}', inline=True)

    return embed