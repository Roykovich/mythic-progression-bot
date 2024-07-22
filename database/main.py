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
    db.execute('CREATE TABLE IF NOT EXISTS orders (id GUID PRIMARY KEY, order_id TEXT, message_id INTEGER, thread_id INTEGER, creator_id INTEGER, order_name TEXT, description TEXT, amount INTEGER, payment TEXT, boostmode TEXT, region TEXT, traders TEXT, keystone_level INTEGER, runs INTEGER, timed TEXT, streaming TEXT, class_and_spec TEXT, faccion TEXT, realm TEXT, custom_name TEXT, battletag TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS applications (id GUID PRIMARY KEY, order_id TEXT, message_id INTEGER, user_id INTEGER, role TEXT, raiderio INTEGER)')
    db.execute('CREATE TABLE IF NOT EXISTS orders_in_progress (id GUID PRIMARY KEY, order_id TEXT, message_id INTEGER, thread_id INTEGER, creator_id INTEGER, tank TEXT, tank_raiderio INTEGER, healer TEXT, healer_raiderio INTEGER, first_dps TEXT, first_dps_raiderio INTEGER, second_dps TEXT, second_dps_raiderio INTEGER)')
