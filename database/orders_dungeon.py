import uuid
from database.main import get_cursor

db = get_cursor()

def create_order(info):
    new_order_id = uuid.uuid4()
    new_applicant_id = uuid.uuid4()
    db.execute('''
        INSERT INTO orders (
            id, order_id, message_id, thread_id, creator_id, order_name,
            description, amount, payment, boostmode, region, traders,
            keystone_level, runs, timed, streaming, class_and_spec,
            faccion, realm, custom_name, battletag
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    ''', (
        new_order_id, info['order_id'], info['message_id'], info['thread_id'],
        info['creator_id'], info['order_name'], info['description'], info['amount'],
        info['payment'], info['boostmode'], info['region'], info['traders'],
        info['keystone_level'], info['runs'], info['timed'], info['streaming'],
        info['class_and_spec'], info['faccion'], info['realm'], info['custom_name'],
        info['battletag']
    ))

    db.execute('''
        INSERT INTO orders_in_progress (
            id, order_id, message_id, thread_id, creator_id
        ) VALUES (
            ?, ?, ?, ?, ?
        )
    ''', (
        new_applicant_id, info['order_id'], info['message_id'], info['thread_id'], info['creator_id']
    ))

    print(f'Orden [{info['order_id']}] creado con el id {new_order_id}')

def accept_applicant_to_order(order_id, user_id, role):
    lookup_role = 'dps' if role == 'first_dps' or role == 'second_dps' else role
    applicant = db.execute('SELECT raiderio FROM applications WHERE order_id = ? AND user_id = ? AND role = ?', (order_id, user_id, lookup_role)).fetchone()

    if role == 'tank':
        db.execute('UPDATE orders_in_progress SET tank = ?, tank_raiderio = ? WHERE order_id = ?', (user_id, applicant[0], order_id,))
        # todo agregar llamada para eliminar de la tabla applications
    elif role == 'first_dps':
        db.execute('UPDATE orders_in_progress SET first_dps = ?, first_dps_raiderio = ? WHERE order_id = ?', (user_id, applicant[0], order_id,))
        # todo agregar llamada para eliminar de la tabla applications
    elif role == 'second_dps':
        db.execute('UPDATE orders_in_progress SET second_dps = ?, second_dps_raiderio = ? WHERE order_id = ?', (user_id, applicant[0], order_id,))
        # todo agregar llamada para eliminar de la tabla applications
    else:
        db.execute('UPDATE orders_in_progress SET healer = ?, healer_raiderio = ? WHERE order_id = ?', (user_id, applicant[0], order_id,))
        # todo agregar llamada para eliminar de la tabla applications

    order = db.execute('SELECT * FROM orders_in_progress WHERE order_id = ?', (order_id,)).fetchone()

    return order 

def check_order_full(order_id):
    order = db.execute('SELECT tank, healer, first_dps, second_dps FROM orders_in_progress WHERE order_id = ?', (order_id,)).fetchone()

    if order[0] and order[1] and order[2] and order[3]:
        return order
    else:
        return False
    
def check_if_booster_is_already_in_order(order_id, user_id):
    # Esto va a retornar un 0 si no esta en la orden y un 1 si ya esta en la orden
    booster = db.execute('SELECT count(1) FROM orders_in_progress WHERE order_id = ? AND (tank = ? OR healer = ? OR first_dps = ? OR second_dps = ?)', (order_id, user_id, user_id, user_id, user_id)).fetchone()
    return booster[0]
        
def get_order_info(order_id):
    order = db.execute('SELECT order_id, order_name, description, amount, payment, boostmode, region, traders, keystone_level, runs, timed, streaming, class_and_spec, faccion, realm, custom_name, battletag, creator_id FROM orders WHERE order_id = ?', (order_id,)).fetchone()
    return order