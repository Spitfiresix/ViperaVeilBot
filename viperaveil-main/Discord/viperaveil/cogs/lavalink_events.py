"""
Event handler for lavalink server
Uses variables stored in self.bot.lavalink
"""
import asyncio
import json
import logging
import wavelink
import sponsorblock as sb

import discord

from discord.ext import commands
from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Skip import DBSkip

from viperaveil.utilities.lavalink.eventend import serverParams, \
    singleLoop, queueLoop, noTrack, playNext

logger = logging.getLogger('discord')


class Track(wavelink.Track): # pylint: disable=too-few-public-methods
    """Wavelink Track object with a requester attribute."""

    __slots__ = ('requester', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get('requester')


class LavalinkEvents(commands.Cog):
    """
    Class for Lavalink events
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @commands.Cog.listener()
    async def on_track_start(self, payload):
        """
        Called when track starts playing
        """


        with open("configuration.json", "r", encoding="utf-8") as config:
            data = json.load(config)
            sponsorblock = data["sponsorblock"]

        # Sponsorblock
        if sponsorblock:
            current_track = DBQueue(
                self.bot.db_connection).getCurrentSong(
                payload.player.guild_id)[4]
            sb_client = sb.Client()
            segments = None

            try:
                segments = sb_client.get_skip_segments(
                    current_track, category="music_offtopic")
            except BaseException: # pylint: disable=broad-except
                pass

            while True:
                # Stop if it's another track
                track = DBQueue(
                    self.bot.db_connection).getCurrentSong(
                    payload.player.guild_id)[4]
                if track != current_track:
                    break

                current_position = payload.player.position
                if segments:
                    for segment in segments:
                        if current_position >= segment.start * 1000 <= current_position \
                            <= segment.end * 1000:
                            await payload.player.seek(segment.end * 1000)
                await asyncio.sleep(0.5)

    @commands.Cog.listener()
    async def on_wavelink_track_stuck(self, player: wavelink.player, track: Track, reason):
        """
        Called when track gets stuck
        """
        print(f'Track stuck: {reason}')
        await LavalinkEvents.on_player_stoped(self, player, track)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.player, track: Track, reason):
        """
        Called when track ends
        """
        print(f'Track ended: {reason}')
        await LavalinkEvents.on_player_stoped(self, player, track)

    @commands.Cog.listener()
    async def on_wavelink_track_exception(self, player: wavelink.player, track: Track, error):
        """
        Called when track has an error
        """
        print(f'Track errored: {error}')
        await LavalinkEvents.on_player_stoped(self, player, track)

    async def on_player_stoped(self, player: wavelink.Player, track: Track):
        """
        Function for moving queue along
        """
        server_parameters = serverParams(self, player)
        is_loop, is_loop_queue, is_shuffle = \
            server_parameters[2], server_parameters[3], server_parameters[4]
        # Clear the skip DB
        DBSkip(self.bot.db_connection).clear(player.guild.id)
        # If Single Loop Enabled
        if is_loop == 1:
            await singleLoop(self, player)
            return
        # Remove former if it exists
        DBQueue(self.bot.db_connection).removeFormer(player.guild.id)
        # Move currently playing to former
        DBQueue(self.bot.db_connection).updatePlayingToFormer(player.guild.id)
        # If Queue Loop Enabled
        if is_loop_queue == 1:
            queueLoop(self, player)
        # If Shuffle Enabled
        if is_shuffle == 1:
            track = DBQueue(
                self.bot.db_connection).getRandomSong(
                player.guild.id)
        else:
            track = DBQueue(self.bot.db_connection).getNextSong(player.guild.id)
        # If no more songs in queue
        if track is None:
            await noTrack(self, player)
            return
        # Play next song in queue
        await playNext(self, player, track)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """
        Called when Wavelink node is available
        """
        print(f'Lavalink node {node.identifier} is ready!')

        # Restart the queue and playing music
        # with open("logoutData.json", "r") as logoutData:
        #     logoutData = json.load(logoutData)

        # serversInQueue = DBQueue(self.bot.db_connection).displayAllPlaying()

        # if serversInQueue:
        #     for server in serversInQueue:
        #         serverID = int(server[0])
        #         if str(serverID) in logoutData:
        #             voiceChannelID = logoutData[str(serverID)]
        #             voiceChannel = self.bot.get_channel(int(voiceChannelID))
        #             if voiceChannel:
        #                 # Get the track
        #                 track = await node.get_tracks(server[4])
        #                 if track:
        #                     track = track[0]
        #                     track = Track(track.id, track.info, requester=server[2])

        #                     # Play the track
        #                     player = node.get_player(serverID)
        #                     if player:
        #                         await player.play(track)


def setup(bot):
    """Imports Cog class on module import"""
    bot.add_cog(LavalinkEvents(bot))
