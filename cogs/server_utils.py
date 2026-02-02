import discord
from discord.ext import commands
from discord import app_commands

class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="Status", description="Checks server status")
    async def ping(self, interaction: discord.Interaction):
        #todo
        pass

async def setup(bot):
    await bot.add_cog(ServerUtils(bot))