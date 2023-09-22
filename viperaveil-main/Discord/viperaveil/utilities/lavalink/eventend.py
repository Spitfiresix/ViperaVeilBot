import discord
from discord.ext import commands
import wavelink
import sponsorblock as sb
import asyncio
import json

from viperaveil.utilities.playTrack import playTrack

from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Server import DBServer
from viperaveil.utilities.database.Skip import DBSkip


def serverParams(self, player: wavelink.Player):
    return DBServer(self.bot.db_connection).displayServer(player.guild.id)


async def singleLoop(self, player: wavelink.Player):
    currentTrack = DBQueue(
        self.bot.db_connection).getCurrentSong(
        player.guild.id)
    try:
        requester, channelID, track = currentTrack[3], currentTrack[4], currentTrack[6]
    except BaseException:
        return
    channel = self.bot.get_channel(int(channelID))
    track = await self.bot.wavelink.get_tracks(cls=wavelink.Track, query=track)
    track = track[0]
    await playTrack(self, channel, player, track, requester)
    return


def queueLoop(self, player: wavelink.Player):
    formerTrack = DBQueue(self.bot.db_connection).displayFormer(player.guild.id)
    try:
        requester, channelID, track, title, duration, thumb = \
            formerTrack[3], formerTrack[4], formerTrack[5], \
                formerTrack[6], formerTrack[7], formerTrack[8]
    except BaseException:
        return
    channel: discord.TextChannel = self.bot.get_channel(int(channelID))
    futureIndex = DBQueue(
        self.bot.db_connection).getFutureIndex(
        player.guild.id)
    futureIndex += 1
    DBQueue(
        self.bot.db_connection).add(
        player.guild.id,
        False,
        requester,
        channel.id,
        player.channel.id,
        track,
        title,
        duration,
        thumb,
        futureIndex)


async def noTrack(self, player: wavelink.Player):
    currentTrack = DBQueue(
        self.bot.db_connection).getCurrentSong(
        player.guild.id)
    if currentTrack is None:
        currentTrack = DBQueue(
        self.bot.db_connection).displayFormer(
        player.guild.id)
    try:
        channelID = currentTrack[4]
        channel: discord.TextChannel = self.bot.get_channel(int(channelID))
        await channel.send(f"{self.bot.emoji_list.false} Disconnected because the queue is empty!", delete_after=12)
        await player.disconnect()
    except BaseException:
        pass
    if hasattr(self.bot, 'lastPlayingSong'):
        try:
            await self.bot.lastPlayingSong.delete()
        except BaseException:
            pass
    DBQueue(self.bot.db_connection).removeFormer(player.guild.id)


async def playNext(self, player: wavelink.Player, track):
    id, server, isPlaying, requester, channel_id, track_url, title, duration, thumb, index = track
    channel: discord.TextChannel = self.bot.get_channel(int(channel_id))
    DBQueue(self.bot.db_connection).setIsPlaying(player.guild.id, index)
    await playTrack(self, channel, player, track_url, requester)
