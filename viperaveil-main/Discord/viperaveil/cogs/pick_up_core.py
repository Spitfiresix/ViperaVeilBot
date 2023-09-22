"""
Pick-up Server Core

Contains core functionality for the pick-up scrim system
"""

import discord
import logging
# from discord import app_commands, ui, Interaction
from discord.ext import commands, tasks
logger = logging.getLogger('discord')

from viperaveil.lib.views.viperaPickUp import pickUpEmbedView
from viperaveil.lib.cogs.vipera.embed import viperaPickupEmbed

class PickUpCore(commands.Cog):
    """
    Class for drop-in
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')
        #PickUpCore.update_vipera_pickup.start(self)  # pylint: disable=no-member

    # @tasks.loop(hours=24.0)
    # async def update_vipera_pickup(self):
    #     """Update Vipera Info embed on loop"""
    #     vipera_guild: discord.Guild = \
    #         self.bot.get_guild(303245408539246603)
    #     vipera_pickup_channel: discord.TextChannel = \
    #         vipera_guild.get_channel(1074878042712834199)
    #     vipera_pickup_message: discord.Message = \
    #         vipera_pickup_channel.get_partial_message(1076566809492344842)
    #     embed = await viperaPickupEmbed(self)
    #     self.bot.pickup_message = await vipera_pickup_message.edit(embed=embed, view=pickUpEmbedView(self.bot))


def setup(bot):
    """Imports Cog class on class import"""
    bot.add_cog(PickUpCore(bot))
