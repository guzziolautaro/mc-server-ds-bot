import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

from db_manager import DBManager
from network_manager import NetworkManager

load_dotenv()

class Bot(commands.Bot):
    def __init__(self, db_path):
        intents = discord.Intents.default()
        intents.message_content = True
        self.db = DBManager(db_path)
        self.network = NetworkManager()
        super().__init__(command_prefix=None, intents=intents)

    async def setup_hook(self):
        await self.db.setup()
        await self.load_extension('cogs.config')
        await self.load_extension('cogs.server_utils')

        @self.tree.error
        async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
            if isinstance(error, app_commands.CheckFailure):
                if interaction.response.is_done():
                    await interaction.followup.send(f":red_circle: {error}", ephemeral=True)
                else:
                    await interaction.response.send_message(f":red_circle: {error}", ephemeral=True)
            else:
                print(f"App Command Error: {error}")

        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')

    async def close(self):
        await self.db.close()
        if hasattr(self, 'network'):
            await self.network.close()
        await super().close()

bot = Bot("bot_data.db")
bot.run(os.getenv('TOKEN'))