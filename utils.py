import discord
from discord import app_commands

def has_guild_setup():
    async def predicate(interaction: discord.Interaction) -> bool:
        guild_data = await interaction.client.db.get_guild_settings(interaction.guild_id)
        
        if guild_data and guild_data["sv_ip"] and guild_data["token"]:
            interaction.extras['guild_settings'] = guild_data
            return True
        
        raise app_commands.CheckFailure("An Ip and Token have to be set to use this command")
    
    return app_commands.check(predicate)

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