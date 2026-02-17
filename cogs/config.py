import discord
import inspect
import secrets
from discord.ext import commands
from discord import app_commands
from network_manager import MinecraftNetworkError
from utils import has_guild_setup, ConfirmLink

class Config(commands.GroupCog, name="config"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_ip", description="Set the server IP address")
    @app_commands.default_permissions(administrator=True)
    async def set_ip(self, interaction: discord.Interaction, ip: str):

        await self.bot.db.update_guild_data(interaction.guild.id, sv_ip=ip)
        await interaction.response.send_message(f"Server IP updated to: `{ip}`", ephemeral=True)

    @app_commands.command(name="generate_token", description="Generate a new token")
    @app_commands.default_permissions(administrator=True)
    async def generate_token(self, interaction: discord.Interaction):

        view = ConfirmLink()

        await interaction.response.send_message(
            "This will overwrite any existing token. Continue?", 
            view=view, 
            ephemeral=True
        )
        await view.wait()

        if view.value:
            new_token = secrets.token_hex(16)

            await self.bot.db.update_guild_data(interaction.guild.id, token=new_token)
            await interaction.followup.send(inspect.cleandoc(f"""
                                                For security reasons this token will only be showed once
                                                Server Token updated to: `{new_token}`
                                            """)
                                            , ephemeral=True)
    
    @app_commands.command(name="sync", description="Syncs and verifies the server IP and TOKEN")
    @app_commands.default_permissions(administrator=True)
    @has_guild_setup()
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        GUILD_SETTINGS = interaction.extras['guild_settings']

        try:
            response = await self.bot.network.send_request(
                ip=GUILD_SETTINGS["sv_ip"],
                port=GUILD_SETTINGS["sv_port"],
                token=GUILD_SETTINGS["token"], 
                action="sync"
            )

            await self.bot.db.update_guild_data(interaction.guild_id, verified=True)
            await interaction.followup.send(f"Sync successful. Server message: `{response}`", ephemeral=True)
                

        except MinecraftNetworkError as e:
            await interaction.followup.send(f"{e.message}", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)
            

async def setup(bot):
    await bot.add_cog(Config(bot))