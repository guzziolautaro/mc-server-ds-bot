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
                description=data,
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

async def setup(bot):
    await bot.add_cog(ServerUtils(bot))