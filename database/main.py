import sqlite3
import uuid
import random
import settings

sqlite3.register_adapter(uuid.UUID, lambda u: u.bytes_le)
sqlite3.register_converter("GUID", lambda b: uuid.UUID(bytes_le=b))

connection = sqlite3.connect(
    'mythic.db', 
    isolation_level=None, 
    detect_types=sqlite3.PARSE_DECLTYPES
)
db = connection.cursor()

def get_cursor():
    return db

def create_tables():
    db.execute('CREATE TABLE IF NOT EXISTS orders (id GUID PRIMARY KEY, order_id TEXT, message_id INTEGER, thread_id INTEGER, creator_id INTEGER, tank TEXT, healer TEXT, first_dps TEXT, second_dps TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS applications (id GUID PRIMARY KEY, order_id TEXT, message_id INTEGER, user_id INTEGER, role TEXT, raiderio INTEGER)')
