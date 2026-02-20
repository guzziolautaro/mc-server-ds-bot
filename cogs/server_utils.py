import discord
from discord.ext import commands
from discord import app_commands
from network_manager import MinecraftNetworkError
from utils import has_guild_setup, has_server_synced

class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Checks server status")
    @has_server_synced()
    async def status(self, interaction: discord.Interaction):
        await interaction.response.defer()

        GUILD_SETTINGS = interaction.extras['guild_settings']
        
        try:
            data = await self.bot.network.send_request(
                ip=GUILD_SETTINGS["sv_ip"],
                port=GUILD_SETTINGS["sv_port"],
                token=GUILD_SETTINGS["token"], 
                action="status"
            )
            embed = discord.Embed(
                title=":green_circle: Server Online",
                description=f"Online: {data.get("online", 0)}/{data.get("max", 0)}",
                color=discord.Color.green()
            )
            embed.set_footer(text=GUILD_SETTINGS["sv_ip"])
            embed.timestamp = discord.utils.utcnow()
            await interaction.followup.send(embed=embed)

        except MinecraftNetworkError as e:
            embed = discord.Embed(
                title=":red_circle: Server offline or unreachable",
                description=e.message,
                color=discord.Color.red()
            )
            embed.set_footer(text=GUILD_SETTINGS["sv_ip"])
            embed.timestamp = discord.utils.utcnow()
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)

    @app_commands.command(name="broadcast", description="Sends a global server message")
    @app_commands.default_permissions(administrator=True)
    @has_server_synced()
    async def broadcast(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)

        GUILD_SETTINGS = interaction.extras['guild_settings']
        params = {
            'message': message
        }

        try:
            data = await self.bot.network.send_request(
                ip=GUILD_SETTINGS["sv_ip"],
                port=GUILD_SETTINGS["sv_port"],
                token=GUILD_SETTINGS["token"], 
                action="broadcast",
                params=params
            )
            
            await interaction.followup.send("Broadcast: " + data.get("status", "unknown"))

        except MinecraftNetworkError as e:
            await interaction.followup.send("Server offline or unreachable")
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)
        

async def setup(bot):
    await bot.add_cog(ServerUtils(bot))