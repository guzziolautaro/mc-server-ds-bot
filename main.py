import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

from db_manager import DBManager

load_dotenv()

class Bot(commands.Bot):
    def __init__(self, db_path):
        intents = discord.Intents.default()
        intents.message_content = True
        self.db = DBManager(db_path)
        super().__init__(command_prefix=None, intents=intents)

    async def setup_hook(self):
        await self.db.setup()
        await self.load_extension('cogs.config')
        await self.load_extension('cogs.server_utils')
        await self.tree.sync()


bot = Bot("bot_data.db")
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

bot.run(os.getenv('TOKEN'))