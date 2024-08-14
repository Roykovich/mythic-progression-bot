import uuid
from database.main import get_cursor

db = get_cursor()

def register_user(email, user_id, wallet_id):
    new_user_id = uuid.uuid4()
    db.execute('INSERT INTO boosters (id, user_id, email, wallet_id, role, booster_points) VALUES (?, ?, ?, ?, ?, ?)', (new_user_id, user_id, email, wallet_id, 'Booster', 0))
    print(f'Usuario [{email}] creado con el id {new_user_id}')

async def get_wallet_by_user_id(boosters):
    wallets_ids = []
    for booster in boosters:
        if not booster:
            print('[!] Booster is None')
            continue
        print(f'[+] Booster: {booster} ({booster.id})')
        wallet = db.execute('SELECT wallet_id, user_id FROM boosters WHERE user_id = ?', (booster.id,)).fetchone()
        print(f'[+] Wallet encontrada: {wallet}')
        if not wallet:
            print('[!] Wallet not found')
            continue

        wallets_ids.append(wallet)

    return wallets_ids
