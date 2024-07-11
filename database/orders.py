import uuid
from database.main import get_cursor

db = get_cursor()

def create_order(order_id, message_id, thread_id, creator_id):
    # TODO Agregar un logger
    # TODO Agregar un try except
    # TODO Agregar un condicional para ver si ya hay una orden con esa id
    new_order_id = uuid.uuid4()
    db.execute('INSERT INTO orders (id, order_id, message_id, thread_id, creator_id) VALUES (?, ?, ?, ?, ?)', (new_order_id, order_id, message_id, thread_id, creator_id))
    print(f'Orden [{order_id}] creado con el id {new_order_id}')

def accept_applicant_to_order(order_id, user_id, role):
    applicants = db.execute('SELECT * FROM orders INNER JOIN applications ON orders.order_id = applications.order_id WHERE orders.order_id = ? AND applications.user_id = ?', (order_id, user_id,))
    # for applicant in applicants:
    #     print(applicant)
    return 
