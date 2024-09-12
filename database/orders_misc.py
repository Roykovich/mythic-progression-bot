import uuid
from database.main import get_cursor

db = get_cursor()

def create_misc_order(info):
    new_order_id = uuid.uuid4()
    db.execute('''
        INSERT INTO misc_orders (
            id, order_id, message_id, thread_id, creator_id, order_name,
            description, amount, payment, boostmode, region, type,
            players, streaming, class_and_spec, faccion,
            realm, custom_name, battletag
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    ''', (
        new_order_id, info['order_id'], info['message_id'], info['thread_id'],
        info['creator_id'], info['order_name'], info['description'], info['amount'],
        info['payment'], info['boostmode'], info['region'], info['type'],  
        info['players'], info['streaming'], info['class_and_spec'], info['faccion'], 
        info['realm'], info['custom_name'], info['battletag']
    ))

    print(f'Orden [{info['order_id']}] creado con el id {new_order_id}')


async def accept_misc_applicant_to_order(order_id, user_id):
    db.execute('UPDATE applications SET selected_status = ? WHERE order_id = ? AND user_id = ?', (1, order_id, user_id))

    order = db.execute('SELECT message_id FROM misc_orders WHERE order_id = ?', (order_id,)).fetchone()

    return order