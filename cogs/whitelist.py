import discord
from discord.ext import commands
from discord import app_commands
from network_manager import MinecraftNetworkError
from utils import has_server_synced

class Whitelist(commands.GroupCog, name="whitelist"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="add", description="Adds a Player name to the whitelist")
    @app_commands.default_permissions(administrator=True)
    @has_server_synced()
    async def add(self, interaction: discord.Interaction, name: str):
        await interaction.response.defer(ephemeral=True)

        GUILD_SETTINGS = interaction.extras['guild_settings']
        params = {
            'operation': 'add',
            'name': name
        }

        try:
            data = await self.bot.network.send_request(
                ip=GUILD_SETTINGS["sv_ip"],
                port=GUILD_SETTINGS["sv_port"],
                token=GUILD_SETTINGS["token"], 
                action="whitelist",
                params=params
            )
            
            match data.get("status", "unknown"):
                case "unknown":
                    await interaction.followup.send(":red_circle: Whitelist unknown error")
                case "unavailable":
                    await interaction.followup.send(":yellow_circle: Whitelist not enabled on this server")
                case "success":
                    await interaction.followup.send(":green_circle: Player name added to the whitelist")
                case "conflict":
                    await interaction.followup.send(":yellow_circle: Player name already on the whitelist")

        except MinecraftNetworkError as e:
            await interaction.followup.send("Server offline or unreachable")
        except Exception as e:
            await interaction.followup.send(f"An unexpected error occurred: {e}", ephemeral=True)

    @app_commands.command(name="remove", description="Removes a Player name from the whitelist")
    @app_commands.default_permissions(administrator=True)
    @has_server_synced()
    async def remove(self, interaction: discord.Interaction, name: str):
        #todo
        pass

    @app_commands.command(name="list", description="lists all Player names in the whitelist")
    @app_commands.default_permissions(administrator=True)
    @has_server_synced()
    async def list(self, interaction: discord.Interaction):
        #todo
        pass

async def setup(bot):
    await bot.add_cog(Whitelist(bot))