import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
EXIT_DAMES_CODE = os.getenv("EXIT_DAMES_CODE") or "EXIT_DAMES_GAME"
bot = commands.Bot(command_prefix = "/")
