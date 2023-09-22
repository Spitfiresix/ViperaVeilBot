"""
Vipera SC Utilities

For use with commands that use game assets/information
"""

import discord
import logging
# from discord import app_commands, ui, Interaction
from discord.ext import commands
logger = logging.getLogger('discord')


class ViperaSCUtility(commands.Cog):
    """
    Cog description should go here
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name="merit",
                          description="Calculate merits required for your sentence")
    @commands.cooldown(1, 5, commands.BucketType.member)
    @discord.option(name='hours', input_type=int, description='Hours of sentence left: 0-∞', min_value=0)
    @discord.option(name='minutes', input_type=int, description='Minutes of sentence left: 0-60', min_value=0, max_value=60)
    @discord.option(name='seconds', input_type=int, description='Seconds of sentence left: 0-60', min_value=0, max_value=60)
    async def merit(self, ctx: discord.Interaction, hours: int, minutes: int, seconds: int):
        totalmerits = 0
        totalmerits += hours * 3600
        totalmerits += minutes * 60
        totalmerits += seconds
        await ctx.response.send_message(content=f'You need: {totalmerits} merits to complete your sentence', delete_after=3600)



def setup(bot):
    """Imports Cog class on class import"""
    bot.add_cog(ViperaSCUtility(bot))
