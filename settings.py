import pathlib, os
import discord
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = pathlib.Path(__file__).parent
COGS_DIR = ROOT_DIR / 'cogs'

TOKEN = os.getenv("TOKEN")

GUILD_ID = discord.Object(id=int(os.getenv("GUILD_ID")))
ORDER_CHANNEL_ID = int(os.getenv("ORDER_CHANNEL_ID"))
COMMAND_CHANNEL_ID = int(os.getenv("COMMAND_CHANNEL_ID"))
ORDER_STARTED_ID = int(os.getenv("ORDER_STARTED_ID"))

ROLE_SERVER_STAFF_ID = os.getenv("ROLE_SERVER_STAFF_ID")
ROLE_DEVELOPER_ID = os.getenv("ROLE_DEVELOPER_ID")
ROLE_MASTER_BOOSTER_ID = os.getenv("ROLE_MASTER_BOOSTER_ID")
ROLE_ELITE_BOOSTER_ID = os.getenv("ROLE_ELITE_BOOSTER_ID")
ROLE_VETERAN_BOOSTER_ID = os.getenv("ROLE_VETERAN_BOOSTER_ID")
ROLE_GOLD_BOOSTER_ID = os.getenv("ROLE_GOLD_BOOSTER_ID")
ROLE_BOOSTER_ID = os.getenv("ROLE_BOOSTER_ID")
ROLE_RAIDER_ID = os.getenv("ROLE_RAIDER_ID")
ROLE_SUPPLIER_ID = os.getenv("ROLE_SUPPLIER_ID")

WP_SWINGS_CLIENT = os.getenv("WP_SWINGS_CLIENT")
WP_SWINGS_SECRET = os.getenv("WP_SWINGS_SECRET")
