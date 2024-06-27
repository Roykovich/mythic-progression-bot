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
ROLE_SERVER_STAFF_ID = int(os.getenv("ROLE_SERVER_STAFF_ID"))