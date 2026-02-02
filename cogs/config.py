import discord
import inspect
import secrets
from discord.ext import commands
from discord import app_commands

class ConfirmLink(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):

        self.value = True
        self.stop()
        await interaction.response.edit_message(view=None)

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        
        self.value = False
        self.stop()
        await interaction.response.edit_message(content="Action cancelled", view=None)

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_ip", description="Set the server IP address")
    @app_commands.default_permissions(administrator=True)
    async def set_ip(self, interaction: discord.Interaction, ip: str):

        await self.bot.db.update_ip(interaction.guild.id, ip)
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

            await self.bot.db.update_token(interaction.guild.id, new_token)
            await interaction.followup.send(inspect.cleandoc(f"""
                                                For security reasons this token will only be showed once
                                                Server Token updated to: `{new_token}`
                                            """)
                                            , ephemeral=True)
            

async def setup(bot):
    await bot.add_cog(Config(bot))