import random
import uuid
import re
from database.main import get_cursor

db = get_cursor()

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


def is_already_applicated(order_id, user_id, role):
    result = db.execute('SELECT user_id FROM applications WHERE order_id = ? AND user_id = ? AND role = ?', (order_id, user_id, role)).fetchone()

    return result

async def create_application(order_id, message_id, user_id, role, char_class, raiderio):
    new_application_id = uuid.uuid4()
    db.execute('''
        INSERT INTO applications (
            id, order_id, message_id, user_id, role, class, raiderio
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?
        )
    ''', (
        new_application_id, order_id, message_id, user_id, role, char_class, raiderio
    ))

    print(f'Aplicación [{new_application_id}] creada para la orden [{order_id}]')


def cancel_application(order_id, user_id):
    result = db.execute('DELETE FROM applications WHERE order_id = ? AND user_id = ?', (order_id, user_id)).rowcount

    return result


def get_role_applications(order_id, role):
    applications = db.execute('SELECT count(*) FROM applications WHERE order_id = ? AND role = ?', (order_id, role)).fetchall()
    return applications[0][0]


def update_staff_applicants_fields(embed, order_id, accepted=False, booster=None) -> None:
    # Si el Booster estaba aceptado, tambien cambia esos campos en el embed del Staff
    if accepted:
        db.execute('''
            DELETE FROM orders_in_progress
            WHERE order_id = ? AND (tank = ? OR healer = ? OR first_dps = ? OR second_dps = ?)
        ''', (order_id, booster, booster, booster, booster))

        accepted_tank = embed.fields[12].value
        accepted_healer = embed.fields[13].value
        accepted_dps = embed.fields[14].value
        embed.set_field_at(12, name=embed.fields[12].name, value=remove_accepted_applicant(booster, accepted_tank), inline=True)
        embed.set_field_at(13, name=embed.fields[13].name, value=remove_accepted_applicant(booster, accepted_healer), inline=True)
        embed.set_field_at(14, name=embed.fields[14].name, value=remove_accepted_applicant(booster, accepted_dps), inline=True)
        return
    
    boosters = display_booster_applications(order_id)
    
    embed.set_field_at(9, name=embed.fields[9].name, value=boosters['tank'], inline=True)
    embed.set_field_at(10, name=embed.fields[10].name, value=boosters['healer'], inline=True)
    embed.set_field_at(11, name=embed.fields[11].name, value=boosters['dps'], inline=True)

    return


def update_applicants_fields(embed, role, order_id):
    amount = get_role_applications(order_id, role)
    field = 9 if role == 'tank' else 10 if role == 'healer' else 11
    replacement = re.sub(r'\(\d\)', f'({amount})', embed.fields[field].name)
    embed.set_field_at(field, name=replacement, value=f'{'0/2' if role == 'dps' else '0/1'}', inline=True)


def update_booster_applicants_fields(embed, role):
    # Dependiendo del role, se actualiza el campo correspondiente
    field = 9 if role == 'tank' else 10 if role == 'healer' else 11
    embed.set_field_at(field, name=embed.fields[field].name, value=f'{'~~2/2~~ **FULL**' if role == 'dps' else '~~1/1~~ **FULL**'}', inline=True)


def display_booster_applications(order_id):
    boosters = db.execute('SELECT user_id, role, class, raiderio FROM applications WHERE order_id = ?', (order_id,)).fetchall()
    values = {
        'tank': '',
        'healer': '',
        'dps': ''
    }

    # Esto ordena los boosters por raiderio
    sorted_boosters = sorted(boosters, key=lambda x: x[2], reverse=True)
    for booster in sorted_boosters:
        if booster[1] == 'tank':
            values['tank'] += f'<@{booster[0]}> ({icons[booster[2]]} {booster[3]})\n'
        elif booster[1] == 'healer':
            values['healer'] += f'<@{booster[0]}> ({icons[booster[2]]} {booster[3]})\n'
        elif booster[1] == 'dps':
            values['dps'] += f'<@{booster[0]}> ({icons[booster[2]]} {booster[3]})\n'
        else:
            print("No se encontro el rol")

    if not values['tank']:
        values['tank'] = 'N/A'
    
    if not values['healer']:
        values['healer'] = 'N/A'

    if not values['dps']:
        values['dps'] = 'N/A'

    return values


def update_accepted_applicants_fields(embed, booster_id, raiderio, role, booster_class):
    field = 12 if role == 'tank' else 13 if role == 'healer' else 14
    embed_name = embed.fields[field].name
    embed_value = embed.fields[field].value
    embed.set_field_at(field, name=embed_name, value=display_accepted_applicants(booster_id, raiderio, role, booster_class, embed_value), inline=True)


def display_accepted_applicants(booster_id, raiderio, role, booster_class, value):
    if not booster_id:
        return 'N/A'
    
    if role == 'first_dps':
        return f'<@{booster_id}> ({icons[booster_class]} {raiderio})'
    elif role == 'second_dps':
        return f'{value}\n<@{booster_id}> ({icons[booster_class]} {raiderio})'
    else:
        return f'<@{booster_id}> ({icons[booster_class]} {raiderio})'


def remove_accepted_applicant(applicant, value):
    new = value
    if len(value) > 35:
        new = re.sub(rf'<@{applicant}> \(.+\)', '', value)
    else:
        new = re.sub(rf'<@{applicant}> \(.+\)', 'N/A', value)

    return new
