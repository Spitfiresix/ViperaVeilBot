import discord
import wavelink

from viperaveil.utilities.Utils import Utils

from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Server import DBServer

from viperaveil.lib.views.viperaMusic import viperaCurrentMusicGenerator


async def sendPlayingSongEmbed(self, ctx: discord.Interaction, track):
    if hasattr(ctx, 'channel'):
        channel = ctx.channel
    else:
        channel = ctx

    player: wavelink.Player = channel.guild.voice_client

    # Volume
    volume = player.volume

    # Track duration
    trackDuration = await Utils().durationFormat(track.duration)

    # Queue size and duration
    queue_size_and_duration = DBQueue(
        self.bot.db_connection).queueSizeAndDuration(
        channel.guild.id)
    if queue_size_and_duration:
        queue_duration = int(queue_size_and_duration[0])
        queue_duration = await Utils().durationFormat(queue_duration)
        queueSize = queue_size_and_duration[1]
    else:
        queueSize = 0
        queue_duration = "00:00"

    # Title
    trackTitle = track.title.replace("*", "\\*")

    # Loop and LoopQueue
    server_params = DBServer(
            self.bot.db_connection).displayServer(
            channel.guild.id)
    isLoop = str(server_params[2])
    isLoopQueue = str(server_params[3])
    isShuffled = str(server_params[4])

    # Embed
    embed = discord.Embed(
        title="Playing Song :",
        description=f"**[{trackTitle}]({track.uri})**",
        color=discord.Colour.dark_green())
    embed.set_thumbnail(url=track.thumb)
    embed.add_field(
        name="Requested by :",
        value=f"`{track.requester}`",
        inline=True)
    embed.add_field(name="Duration :", value=f"`{trackDuration}`", inline=True)
    embed.add_field(name="Volume :", value=f"`{volume} %`", inline=True)
    embed.add_field(
        name="Loop Song :",
        value=isLoop.replace(
            'True',
            f"{self.bot.emoji_list.true}").replace(
            'False',
            f"{self.bot.emoji_list.false}"),
        inline=True)
    embed.add_field(
        name="Loop queue :",
        value=isLoopQueue.replace(
            'True',
            f"{self.bot.emoji_list.true}").replace(
            'False',
            f"{self.bot.emoji_list.false}"),
        inline=True)
    embed.add_field(
        name="Shuffle :",
        value=isShuffled.replace(
            'True',
            f"{self.bot.emoji_list.true}").replace(
            'False',
            f"{self.bot.emoji_list.false}"),
        inline=True)
    embed.add_field(name="Lyrics :", value=f"`/lyrics`", inline=True)
    embed.add_field(
        name="Queue :",
        value=f"`{queueSize} song(s) ({queue_duration})`: \
            [Link](https://www.viperaveil.net/bot/queue?guildid={ctx.guild.id})",
        inline=True)
    # embed.add_field(name="DJ Role :", value=f"`@role`", inline=True)
    TTL = player.track.duration - player.position
    if TTL < 10:
        TTL = player.track.duration
    if player.is_paused():
        isPaused = True
    else:
        isPaused = False
    currentMusicEmbedView: discord.ui.View = viperaCurrentMusicGenerator(
        self.bot, track, isPaused, isLoop, isLoopQueue, isShuffled)
    if currentMusicEmbedView.inPlayPause == discord.ButtonStyle.red:
        TTL = None
    if hasattr(self.bot, 'lastPlayingSong'):
        try:
            self.bot.lastPlayingSong = await self.bot.lastPlayingSong.edit(
                embed=embed, view=currentMusicEmbedView)
            return
        except BaseException:
            try:
                await self.bot.lastPlayingSong.delete()
            except BaseException:
                pass
    self.bot.lastPlayingSong: discord.Message = await channel.send(
        embed=embed, view=currentMusicEmbedView)
    DBServer(self.bot.db_connection).updateMessage(ctx.guild.id, self.bot.lastPlayingSong.id)
