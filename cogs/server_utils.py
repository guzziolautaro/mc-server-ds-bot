import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="status", description="Checks server status")
    async def status(self, interaction: discord.Interaction):
        GUILD_DATA = await self.bot.db.get_guild_settings(interaction.guild_id)

        SERVER_URL = GUILD_DATA[0]
        SECRET_TOKEN = GUILD_DATA[1]

        SERVER_URL = f"http://{SERVER_URL}:8080/bot"

        if SECRET_TOKEN == None:
            await interaction.response.send_message("Token not generated")
            return

        headers = {"Authorization": f"Bearer {SECRET_TOKEN}"}
        payload = {"action": "status"}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(SERVER_URL, json=payload, headers=headers, timeout=5) as response:
                    if response.status == 200:
                        data = await response.text()
                        await interaction.response.send_message(f"**Server Status:** {data}")
                    elif response.status == 403:
                        await interaction.response.send_message("Security Error: Invalid Token.", ephemeral=True)
                    else:
                        await interaction.response.send_message(f"Server returned error code: {response.status}", ephemeral=True)
            except aiohttp.ClientConnectorError:
                await interaction.response.send_message("Could not connect to the server")
            except Exception as e:
                await interaction.response.send_message(f"An unexpected error occurred: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ServerUtils(bot))