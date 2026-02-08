import discord
from discord.ext import commands
from discord import app_commands
from network_manager import MinecraftNetworkError

class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Checks server status")
    async def status(self, interaction: discord.Interaction):
        GUILD_DATA = await self.bot.db.get_guild_settings(interaction.guild_id)
        
        ip = GUILD_DATA["sv_ip"]
        port = GUILD_DATA["sv_port"]
        token = GUILD_DATA["token"]

        if not GUILD_DATA or not token:
            return await interaction.response.send_message("Server not set up.", ephemeral=True)
        
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