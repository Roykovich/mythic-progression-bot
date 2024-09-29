import sqlite3
import uuid

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
    # ORDERS
    db.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id GUID PRIMARY KEY,
            order_id TEXT,
            message_id INTEGER,
            thread_id INTEGER,
            creator_id INTEGER,
            order_name TEXT,
            description TEXT,
            amount INTEGER,
            payment TEXT,
            boostmode TEXT,
            region TEXT,
            traders TEXT,
            keystone_level INTEGER,
            runs INTEGER,
            timed TEXT,
            streaming TEXT,
            class_and_spec TEXT,
            faccion TEXT,
            realm TEXT,
            custom_name TEXT,
            battletag TEXT
        )
    ''')
    
    # APPLICATIONS
    db.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id GUID PRIMARY KEY,
            character_id GUID,
            order_id TEXT,
            message_id INTEGER,
            user_id INTEGER,
            class TEXT,
            role TEXT,
            selected_status INT DEFAULT 0,
            raiderio INTEGER
        )
    ''')
    
    # ORDERS IN PROGRESS
    db.execute('''
        CREATE TABLE IF NOT EXISTS orders_in_progress (
            id GUID PRIMARY KEY,
            order_id TEXT,
            message_id INTEGER,
            thread_id INTEGER,
            creator_id INTEGER,
            tank TEXT,
            tank_class TEXT,
            tank_raiderio INTEGER,
            healer TEXT,
            healer_class TEXT,
            healer_raiderio INTEGER,
            first_dps TEXT,
            first_dps_class TEXT,
            first_dps_raiderio INTEGER,
            second_dps TEXT,
            second_dps_class TEXT,
            second_dps_raiderio INTEGER
        )
    ''')

    
    # BOOSTERS
    db.execute('''
        CREATE TABLE IF NOT EXISTS boosters (
            id GUID PRIMARY KEY,
            user_id INTEGER,
            email TEXT,
            wallet_id TEXT,
            role TEXT,
            booster_points INTEGER
        )
    ''')
    
    # CHARACTERS
    db.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id GUID PRIMARY KEY,
            user_id INTEGER,
            name TEXT,
            region TEXT,
            realm TEXT,
            class TEXT,
            spec TEXT,
            role TEXT,
            faction TEXT,
            dps_raiderio INTEGER,
            tank_raiderio INTEGER,
            healer_raiderio INTEGER,
            ilvl INTEGER
        )
    ''')
    
    # MISC ORDERS
    db.execute('''
        CREATE TABLE IF NOT EXISTS misc_orders (
            id GUID PRIMARY KEY,
            order_id TEXT,
            message_id INTEGER,
            thread_id INTEGER,
            creator_id INTEGER,
            order_name TEXT,
            description TEXT,
            amount INTEGER,
            payment TEXT,
            boostmode TEXT,
            region TEXT,
            type TEXT,
            players TEXT,
            streaming TEXT,
            class_and_spec TEXT,
            faccion TEXT,
            realm TEXT,
            custom_name TEXT,
            battletag TEXT
        )
    ''')
