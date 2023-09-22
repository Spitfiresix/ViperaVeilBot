import discord
from discord import ui, Interaction
from discord.ext import commands
import wavelink

from viperaveil.lib.views.functions.viperaMusic import skip, reload, pause, resume, loop, loopqueue, shuffle

from viperaveil.utilities.Utils import Utils

from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Server import DBServer


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
    queueSizeAndDuration = DBQueue(
        self.bot.db_connection).queueSizeAndDuration(
        channel.guild.id)
    if queueSizeAndDuration:
        queueDuration = int(queueSizeAndDuration[0])
        queueDuration = await Utils().durationFormat(queueDuration)
        queueSize = queueSizeAndDuration[1]
    else:
        queueSize = 0
        queueDuration = "00:00"

    # Title
    trackTitle = track.title.replace("*", "\\*")

    # Loop and LoopQueue
    isLoop = str(
        DBServer(
            self.bot.db_connection).displayServer(
            channel.guild.id)[2])
    isLoopQueue = str(
        DBServer(
            self.bot.db_connection).displayServer(
            channel.guild.id)[3])
    isShuffled = str(
        DBServer(
            self.bot.db_connection).displayServer(
            channel.guild.id)[4])

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
        value=f"`{queueSize} song(s) ({queueDuration})`: [Link](https://www.viperaveil.net/bot/queue?guildid={ctx.guild.id})",
        inline=True)
    # embed.add_field(name="DJ Role :", value=f"`@role`", inline=True)
    TTL = player.track.duration - player.position
    if TTL < 2:
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
            self.bot.lastPlayingSong = await self.bot.lastPlayingSong.edit(embed=embed, view=currentMusicEmbedView)
            return
        except BaseException:
            try:
                await self.bot.lastPlayingSong.delete()
            except BaseException:
                pass
    self.bot.lastPlayingSong: discord.Message = await channel.send(embed=embed, view=currentMusicEmbedView)


def viperaCurrentMusicGenerator(
        bot,
        track,
        isPaused,
        isLooped,
        isQueueLooped,
        isShuffled):
    if isPaused:
        playpause = discord.ButtonStyle.red
    else:
        playpause = discord.ButtonStyle.green
    if isLooped == 'True':
        loopColour = discord.ButtonStyle.green
    else:
        loopColour = discord.ButtonStyle.grey
    if isQueueLooped == 'True':
        queueLoopColour = discord.ButtonStyle.green
    else:
        queueLoopColour = discord.ButtonStyle.grey
    if isShuffled == 'True':
        shuffledColour = discord.ButtonStyle.green
    else:
        shuffledColour = discord.ButtonStyle.grey

    class currentMusicEmbedView(discord.ui.View):
        def __init__(self, bot, track):
            super().__init__(timeout=None)
            self.bot = bot
            self.add_item(discord.ui.Button(label='🔍', url=track.uri))
        inPlayPause = playpause
        inLoopColour = loopColour
        inQueueLoopColour = queueLoopColour
        inShuffleColour = shuffledColour

        @discord.ui.button(custom_id='viperaMusicPrevious',
                           emoji='⏮️', style=discord.ButtonStyle.green)
        async def viperaMusicPrevious(self, button: discord.ui.Button, ctx: discord.Interaction):
            await reload(self, ctx)

        @discord.ui.button(custom_id='viperaMusicPlayPause',
                           emoji='⏯️', style=inPlayPause)
        async def viperaMusicPlayPause(self, button: discord.ui.Button, ctx: discord.Interaction):
            player: wavelink.Player = ctx.guild.voice_client
            if player:
                if player.is_paused():
                    await resume(self, ctx)
                    player: wavelink.Player = ctx.guild.voice_client
                    await sendPlayingSongEmbed(self, ctx, player.track)
                    return
                if player.is_playing():
                    await pause(self, ctx)
                    player: wavelink.Player = ctx.guild.voice_client
                    await sendPlayingSongEmbed(self, ctx, player.track)
                    return
            else:
                return

        @discord.ui.button(custom_id='viperaMusicNext',
                           emoji='⏭️', style=discord.ButtonStyle.green)
        async def viperaMusicNext(self, button: discord.ui.Button, ctx: discord.Interaction):
            await skip(self, ctx)

        @discord.ui.button(custom_id='viperaMusicLoop',
                           emoji='🔂', style=inLoopColour)
        async def viperaMusicLoop(self, button: discord.ui.Button, ctx: discord.Interaction):
            await loop(self, ctx)
            player: wavelink.Player = ctx.guild.voice_client
            await sendPlayingSongEmbed(self, ctx, player.track)

        @discord.ui.button(custom_id='viperaMusicLoopQueue',
                           emoji='🔁', style=inQueueLoopColour)
        async def viperaMusicLoopQueue(self, button: discord.ui.Button, ctx: discord.Interaction):
            await loopqueue(self, ctx)
            player: wavelink.Player = ctx.guild.voice_client
            await sendPlayingSongEmbed(self, ctx, player.track)

        @discord.ui.button(custom_id='viperaMusicShuffle',
                           emoji='🔀', style=shuffledColour)
        async def viperaMusicShuffle(self, button: discord.ui.Button, ctx: discord.Interaction):
            await shuffle(self, ctx)
            player: wavelink.Player = ctx.guild.voice_client
            await sendPlayingSongEmbed(self, ctx, player.track)

    return currentMusicEmbedView(bot, track)
