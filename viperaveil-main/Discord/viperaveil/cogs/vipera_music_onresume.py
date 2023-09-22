"""
Vipera On-Resume Music Cog
"""

from viperaveil.utilities.database.Skip import DBSkip
from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Server import DBServer
from viperaveil.utilities.Check import Check
from viperaveil.utilities.playTrack import playTrack
from viperaveil.utilities.Utils import Utils
import discord
import wavelink
import asyncio
import tekore
import aiohttp
import json
import os

from math import ceil
from discord import ui, Interaction
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, MissingPermissions, CommandNotFound, MissingRequiredArgument, ExpectedClosingQuoteError, BotMissingPermissions
from youtubesearchpython import PlaylistsSearch
from sclib.asyncio import Track, Playlist

import logging
logger = logging.getLogger('discord')

class ViperaTemplate(commands.Cog):
    """
    Initializer for on-resume
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(5)
        class NewCTX(object):
            pass
        for guild in self.bot.guilds:
            currentTrack = DBQueue(
                self.bot.db_connection).getCurrentSong(
                guild.id)
            server_params = DBServer(self.bot.db_connection).displayServer(guild.id)
            if currentTrack:
                ctx = NewCTX()
                ctx.guild: discord.Guild = guild
                ctx.channel: discord.TextChannel = self.bot.get_channel(int(currentTrack[4]))
                channel: discord.VoiceChannel = self.bot.get_channel(int(currentTrack[5]))
                player = await channel.connect(cls=wavelink.Player)
                volume = DBServer(self.bot.db_connection).displayServer(ctx.guild.id)
                await player.set_volume(volume[6])
                self.bot.lastPlayingSong: discord.Message = ctx.channel.get_partial_message(int(server_params[7]))
                await playTrack(self, ctx, player, currentTrack[6], currentTrack[3])

# id, server, "isPlaying", requester, "textChannel", "voiceChannel", track, title, duration, thumb, index

def setup(bot):
    """Imports Cog class on class import"""
    bot.add_cog(ViperaTemplate(bot))
