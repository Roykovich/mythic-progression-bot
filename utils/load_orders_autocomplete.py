import discord
from discord import app_commands
import typing
from database.main import get_cursor

db = get_cursor()

def get_orders_id(orders: list[str], similarities: str) -> list:
    return [order_id for order_id in orders if similarities in order_id][:24]

async def orders_autocomplete(
        interection: discord.Interaction,
        current: str,
) -> typing.List[app_commands.Choice]:
    if not current:
        return []
    
    db.row_factory = lambda cursor, row: row[0]
    orders = db.execute("SELECT order_id FROM orders").fetchall()
    orders_id = []
    order_id_dictionary = get_orders_id(orders, current)


    for order_id in order_id_dictionary:
        orders_id.append(app_commands.Choice(name=order_id, value=order_id))

    if not orders_id:
        orders_id.append(app_commands.Choice(name=current, value=current))

    return orders_id