"""
Vipera Template Cog
To be used as a template for new cogs
Filename should match cog class name

Uncomment the other imports as required
"""

# import discord
import logging
# from discord import app_commands, ui, Interaction
from discord.ext import commands
logger = logging.getLogger('discord')


class ViperaTemplate(commands.Cog):
    """
    Cog description should go here
    """

    def __init__(self, bot):
        self.bot = bot

    # Start code here


def setup(bot):
    """Imports Cog class on class import"""
    bot.add_cog(ViperaTemplate(bot))
