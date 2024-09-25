import discord
from database.booster import get_booster_profile
from utils.raiderio import get_raiderio_profile

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
    'bags': '<:bags:1107428757884637184>',
    'quest': '<:quest:1107428715962572862>'
}

async def generate_character_list(user_id, role, mention):
    result = []
    characters = await get_booster_profile(user_id)

    if len(characters) < 1:
        return None 
    
    # El motivo por el cual uso el indice es porque el valor a veces puede dar resultados iguales
    # Entonces para evitar esto agregamos el indice al valor para que sea unico
    for index, character in enumerate(characters):
        pj = get_raiderio_profile(character[6], character[2].replace(" ", "%20"), character[1])
        ios = {
            'dps': pj['mythic_plus_scores_by_season'][0]['scores']['dps'],
            'tank': pj['mythic_plus_scores_by_season'][0]['scores']['tank'],
            'healer': pj['mythic_plus_scores_by_season'][0]['scores']['healer']
        }
        to_label = f'{character[1]} [{character[4]}] ({character[2]})'
        to_value = f'{index}[{character[3]}] {character[1]} ({ios[role]})'

        result.append(discord.SelectOption(label=to_label, value=to_value, emoji=icons[character[3]], description=f'IO: {ios[role]}'))

    return result