import uuid
import re
from database.main import get_cursor

db = get_cursor()

def is_already_applicated(order_id, user_id):
    result = db.execute('''
        SELECT user_id FROM applications WHERE order_id = ? AND user_id = ?
    ''', (
        order_id, user_id
    )).fetchone()

    return result

async def apply_to_misc_order(order_id, message_id, user_id, role=None, raiderio=None):
    new_application_id = uuid.uuid4()
    db.execute('''
        INSERT INTO applications (
            id, order_id, message_id, user_id, 
            role, raiderio
        ) VALUES (
            ?, ?, ?, ?, ?, ?
        )
    ''', (
        new_application_id, order_id, message_id, user_id, role, raiderio
    ))
    
    print(f'Aplicación [{new_application_id}] creada para la orden [{order_id}]')

def update_staff_applicants_fields_misc(embed, order_id) -> None:    
    boosters = display_booster_applications(order_id)
    
    embed.set_field_at(9, name=embed.fields[9].name, value=' '.join(boosters['first_applicants']), inline=True)
    embed.set_field_at(10, name=embed.fields[10].name, value=' '.join(boosters['second_applicants']), inline=True)
    embed.set_field_at(11, name=embed.fields[11].name, value=' '.join(boosters['third_applicants']), inline=True)

    if len(boosters['fourth_applicants']) > 0:
        embed.set_field_at(12, name='Boosters', value=' '.join(boosters['fourth_applicants']), inline=True)

    if len(boosters['fifth_applicants']) > 0:
        embed.set_field_at(13, name='Boosters', value=' '.join(boosters['fifth_applicants']), inline=True)
    
    if len(boosters['sixth_applicants']) > 0:
        embed.set_field_at(14, name='Boosters', value=' '.join(boosters['sixth_applicants']), inline=True)
    
    return

def display_booster_applications(order_id):
    boosters = db.execute('SELECT user_id FROM applications WHERE order_id = ?', (order_id,)).fetchall()

    values = {
        'first_applicants': [],
        'second_applicants': [],
        'third_applicants': [],
        'fourth_applicants': [],
        'fifth_applicants': [],
        'sixth_applicants': [],
    }

    # ! estoy seguro que esta vaina se puede refactorizar
    for booster in boosters:
        if len(values['fifth_applicants']) > 4:
            values['sixth_applicants'].append(f'<@{booster[0]}>\n')
            continue
        
        if len(values['fourth_applicants']) > 4:
            values['fifth_applicants'].append(f'<@{booster[0]}>\n')
            continue

        if len(values['third_applicants']) > 4:
            values['fourth_applicants'].append(f'<@{booster[0]}>\n')
            continue

        if len(values['second_applicants']) > 4:
            values['third_applicants'].append(f'<@{booster[0]}>\n')
            continue

        if len(values['first_applicants']) > 4:
            values['second_applicants'].append(f'<@{booster[0]}>\n')
            continue

        values['first_applicants'].append(f'<@{booster[0]}>\n')

    if len(values['first_applicants']) == 0:
        values['first_applicants'] = 'N/A'

    if len(values['second_applicants']) == 0:
        values['second_applicants'] = 'N/A'
    
    if len(values['third_applicants']) == 0:
        values['third_applicants'] = 'N/A'

    return values

def update_accepted_applicants_fields_misc(embed, order_id):
    boosters = db.execute('SELECT user_id FROM applications WHERE order_id = ? AND selected_status = ?', (order_id, 1)).fetchall()

    values = {
        'first_applicants': [],
        'second_applicants': [],
        'third_applicants': []
    }

    for booster in boosters:
        if len(values['second_applicants']) > 4:
            values['third_applicants'].append(f'<@{booster[0]}>\n')
            continue
        
        if len(values['first_applicants']) > 4:
            values['second_applicants'].append(f'<@{booster[0]}>\n')
            continue

        values['first_applicants'].append(f'<@{booster[0]}>\n')

        embed.set_field_at(15, name='Selected Boosters', value=' '.join(values['first_applicants']), inline=True)
    
    if len(values['first_applicants']) > 0:
        embed.set_field_at(16, name='Selected Boosters', value=' '.join(values['second_applicants']), inline=True)

    if len(values['second_applicants']) > 0:
        embed.set_field_at(17, name='Selected Boosters', value=' '.join(values['third_applicants']), inline=True)
    
