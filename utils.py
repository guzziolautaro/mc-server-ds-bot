import discord
from discord import app_commands

def has_guild_setup():
    async def predicate(interaction: discord.Interaction) -> bool:
        guild_data = await interaction.client.db.get_guild_settings(interaction.guild_id)
        
        if guild_data and guild_data[0] and guild_data[1]:
            interaction.extras['guild_settings'] = guild_data
            return True
        
        raise app_commands.CheckFailure("Server not set up.")
    
    return app_commands.check(predicate)