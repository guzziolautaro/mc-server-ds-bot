import discord
from discord.ext import commands
from discord import app_commands
from network_manager import MinecraftNetworkError
from utils import has_guild_setup

class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Checks server status")
    @has_guild_setup()
    async def status(self, interaction: discord.Interaction):
        GUILD_SETTINGS = interaction.extras['settings']
        
        ip = GUILD_SETTINGS["sv_ip"]
        port = GUILD_SETTINGS["sv_port"]
        token = GUILD_SETTINGS["token"]
        
        try:
            data = await self.bot.network.send_request(
                ip=ip,
                port=port,
                token=token, 
                action="status"
            )
            await interaction.response.send_message(f"**Server Status:** {data}")

        except MinecraftNetworkError as e:
            await interaction.response.send_message(f"{e.message}", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Unexpected error: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerUtils(bot))