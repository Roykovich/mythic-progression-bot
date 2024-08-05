import random
import uuid
import re
from database.main import get_cursor

db = get_cursor()

def is_already_applicated(order_id, user_id, role):
    result = db.execute('SELECT user_id FROM applications WHERE order_id = ? AND user_id = ? AND role = ?', (order_id, user_id, role)).fetchone()

    return result

def apply_to_order(order_id, message_id, user_id, role, raiderio=random.randint(890, 3500)):
    new_application_id = uuid.uuid4()
    db.execute('INSERT INTO applications (id, order_id, message_id, user_id, role, raiderio) VALUES (?, ?, ?, ?, ?, ?)', (new_application_id, order_id, message_id, user_id, role, raiderio))
    print(f'Aplicación [{new_application_id}] creada para la orden [{order_id}]')

def cancel_application(order_id, user_id):
    result = db.execute('DELETE FROM applications WHERE order_id = ? AND user_id = ?', (order_id, user_id)).rowcount

    return result

def get_applications(order_id, role):
    applications = db.execute('SELECT user_id, raiderio FROM applications WHERE order_id = ? AND role = ?', (order_id, role.lower())).fetchall()

    return applications

def get_role_applications(order_id, role):
    applications = db.execute('SELECT count(*) FROM applications WHERE order_id = ? AND role = ?', (order_id, role)).fetchall()
    return applications[0][0]

def update_staff_applicants_fields(embed, applicants, role):
    # Dependiendo del role, se actualiza el campo correspondiente
    field = 9 if role == 'tank' else 10 if role == 'healer' else 11
    embed.set_field_at(field, name=embed.fields[field].name, value=display_applicants(applicants), inline=True)

def update_applicants_fields(embed, role, order_id):
    amount = get_role_applications(order_id, role)
    field = 9 if role == 'tank' else 10 if role == 'healer' else 11
    replacement = re.sub(r'\(\d\)', f'({amount})', embed.fields[field].name)
    embed.set_field_at(field, name=replacement, value=f'{'0/2' if role == 'dps' else '0/1'}', inline=True)

def update_booster_applicants_fields(embed, role):
    # Dependiendo del role, se actualiza el campo correspondiente
    field = 9 if role == 'tank' else 10 if role == 'healer' else 11
    embed.set_field_at(field, name=embed.fields[field].name, value=f'{'~~2/2~~ **FULL**' if role == 'dps' else '~~1/1~~ **FULL**'}', inline=True)

def display_applicants(applications):
    if len(applications) == 0:
        return 'N/A'

    value = ''
    sorted_applications = sorted(applications, key=lambda x: x[1], reverse=True)
    for application in sorted_applications:
        raiderio = application[1]
        value += f'<@{application[0]}> ({io_colour_checker(raiderio)} {raiderio})\n'
    
    return value

def update_accepted_applicants_fields(embed, applicant, raiderio, role):
    field = 12 if role == 'tank' else 13 if role == 'healer' else 14
    embed_name = embed.fields[field].name
    embed_value = embed.fields[field].value
    embed.set_field_at(field, name=embed_name, value=display_accepted_applicants(applicant, raiderio, role, embed_value), inline=True)


def display_accepted_applicants(applicant, raiderio, role, value):
    print(applicant, raiderio, role, value)
    if not applicant:
        return 'N/A'
    
    if role == 'first_dps':
        return f'<@{applicant}> ({io_colour_checker(int(raiderio))} {raiderio})'
    elif role == 'second_dps':
        return f'{value}\n<@{applicant}> ({io_colour_checker(int(raiderio))} {raiderio})'
    else:
        return f'<@{applicant}> ({io_colour_checker(int(raiderio))} {raiderio})'
    
# ??? Revisar que hice aqui
def update_after_cancel(embed, order_id, role):
    applicants = get_applications(order_id, role)
    update_staff_applicants_fields(embed, applicants, role)


def io_colour_checker(io: int):
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