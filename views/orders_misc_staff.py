import discord
from database.orders_dungeon import check_order_full, get_order_info
from utils.embed_order import order_created_embed
from utils.get_message import get_message

import settings

class OrderStaffMiscView(discord.ui.View):
    @discord.ui.button(label='Complete Selection', emoji='✅', style=discord.ButtonStyle.success, row=1, disabled=True)
    async def complete(self, interaction: discord.Interaction, button: discord.ui.Button):
        ...
        return
    
