import discord
import wavelink

from discord.ext import commands
from discord import ui, Interaction
from datetime import datetime

from viperaveil.utilities.Check import Check
from viperaveil.utilities.Utils import Utils

from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Server import DBServer

from viperaveil.utilities.sendPlayingSongEmbed import sendPlayingSongEmbed

from viperaveil.cogs.viperamusiccore import noResultFound

import logging
logger = logging.getLogger('discord')


class viperamusicqueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name="loop",
                          description="Enable or disable looping for the current song.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def loop(self, ctx: discord.Interaction):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        isLoop = DBServer(self.bot.db_connection).displayServer(ctx.guild.id)[2]

        if isLoop == 1:
            DBServer(self.bot.db_connection).updateLoop(ctx.guild.id, False)
            await ctx.response.send_message(f"{ctx.user.mention} Single loop mode disabled!", delete_after=20)
        else:
            DBServer(self.bot.db_connection).updateLoop(ctx.guild.id, True)
            await ctx.response.send_message(f"{ctx.user.mention} Single loop mode enabled!", delete_after=20)

    @discord.slash_command(name="loopqueue",
                          description="Enable or disable looping for the current queue.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def loopqueue(self, ctx: discord.Interaction):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        isLoopQueue = DBServer(
            self.bot.db_connection).displayServer(
            ctx.guild.id)[3]

        if isLoopQueue == 1:
            DBServer(
                self.bot.db_connection).updateLoopQueue(
                ctx.guild.id, False)
            await ctx.response.send_message(f"{ctx.user.mention} Queue looping mode disabled!", delete_after=20)
        else:
            DBServer(self.bot.db_connection).updateLoopQueue(ctx.guild.id, True)
            await ctx.response.send_message(f"{ctx.user.mention} Queue looping mode enabled!", delete_after=20)

    @discord.slash_command(name="move",
                          description="Move a song in the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    @discord.option(name='indexfrom', input_type=str, description='Starting song location in queue')
    @discord.option(name='indexto', input_type=str, description='Place to move song to in queue')
    async def move(self, ctx: discord.Interaction, indexfrom: str, indexto: str):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        tracks = DBQueue(self.bot.db_connection).display(ctx.guild.id)
        tracksCount = len(tracks)

        if len(tracks) == 0:
            return await ctx.response.send_message(f"{self.bot.emojiList.false} {ctx.user.mention} The queue is empty!", delete_after=20)

        if not indexfrom.isdigit() or not indexto.isdigit():
            return await ctx.response.send_message(f"{self.bot.emojiList.false}{ctx.user.mention} Index have to be a number!", delete_after=20)
        if ((int(indexfrom)) > tracksCount) or ((int(indexto)) > tracksCount):
            return await ctx.response.send_message(f"{self.bot.emojiList.false} {ctx.user.mention} Index is invalid!", delete_after=20)
        if (int(indexfrom) == int(indexto)):
            return await ctx.response.send_message(f"{self.bot.emojiList.false} {ctx.user.mention} Indexes cannot be the same!", delete_after=20)

        indexFromFake = int(indexfrom)
        indexToFake = int(indexto)

        # Get real index
        indexfrom = DBQueue(
            self.bot.db_connection).getIndexFromFakeIndex(
            ctx.guild.id, indexFromFake - 1)
        indexto = DBQueue(
            self.bot.db_connection).getIndexFromFakeIndex(
            ctx.guild.id, indexToFake - 1)

        # Get the track to move
        trackToMove = DBQueue(
            self.bot.db_connection).displaySpecific(
            ctx.guild.id, indexfrom)
        indexfrom = trackToMove[7]

        # Delete the track to move
        DBQueue(self.bot.db_connection).remove(ctx.guild.id, indexfrom)

        if indexfrom < indexto:
            # -1 to each track between trackToMove index and
            DBQueue(
                self.bot.db_connection).updateRemoveOneToEach(
                ctx.guild.id, indexfrom, indexto)
        else:
            # +1 to each track between trackToMove index and
            DBQueue(
                self.bot.db_connection).updateAddOneToEach(
                ctx.guild.id, indexfrom, indexto)

        # Re-create the track
        DBQueue(
            self.bot.db_connection).add(
            trackToMove[0],
            trackToMove[1],
            trackToMove[2],
            trackToMove[3],
            trackToMove[4],
            trackToMove[5],
            trackToMove[6],
            indexto)

        embed = discord.Embed(
            title="Song moved",
            description=f"- [**{trackToMove[5]}**]({trackToMove[4]}) was moved from `{indexFromFake}` to `{indexToFake}`.",
            color=discord.Colour.dark_green(),
            timestamp=datetime.now())
        embed.set_footer(text=ctx.user.name, icon_url=ctx.user.avatar_url)
        await ctx.response.send_message(embed=embed, delete_after=30)

    @discord.slash_command(name="nowplaying",
                          description="Display the current song!")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def nowplaying(self, ctx: discord.Interaction):

        player: wavelink.Player = ctx.guild.voice_client

        if not player:
            return await ctx.response.send_message(f"{ctx.user.mention} There is currently no song playing!", delete_after=20)
        if player:
            if not player.is_playing():
                return await ctx.response.send_message(f"{ctx.user.mention} There is currently no song playing!", delete_after=20)

        await ctx.response.send_message(content='Displaying current song.', delete_after=5)
        await sendPlayingSongEmbed(self, ctx, player.track)

    @discord.slash_command(name="resume",
                          description="Resume the current song.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def resume(self, ctx: discord.Interaction):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        player: wavelink.Player = ctx.guild.voice_client

        if player:
            if not player.is_playing():
                return await ctx.response.send_message(f"{ctx.user.mention} No song is currently playing!", delete_after=20)
        if player.is_paused:
            await player.set_pause(False)
            return await ctx.response.send_message(f"{ctx.user.mention} The song is resumed!", delete_after=20)
        await ctx.response.send_message(f"{ctx.user.mention} The song is already resumed!", delete_after=20)

    @discord.slash_command(name="pause",
                          description="Pause the current song.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def pause(self, ctx: discord.Interaction):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        player: wavelink.Player = ctx.guild.voice_client
        if player:
            if not player.is_playing():
                return await ctx.response.send_message(f"{ctx.user.mention} No song is currently playing!", delete_after=20)
        if not player.is_paused():
            await player.set_pause(True)
            return await ctx.response.send_message(f"{ctx.user.mention} The song is paused!", delete_after=20)
        await ctx.response.send_message(f"{ctx.user.mention} The song is already paused!", delete_after=20)

    @discord.slash_command(name="queue",
                          description="Display the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def queue(self, ctx: discord.Interaction):
        embed = discord.Embed(
            title=f'Link to the queue is here: [Queue](https://www.viperaveil.net/bot/queue?guildid={ctx.guild.id})',
            colour=discord.Colour.dark_green())
        embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        await ctx.response.send_message(embed=embed, delete_after=12)
        # isFirstMessage = True
        # message = ""

        # tracks = DBQueue(self.bot.db_connection).display(ctx.guild.id)

        # if len(tracks) == 0:
        # return await ctx.response.send_message(f"{self.bot.emojiList.false}
        # {ctx.user.mention} The queue is empty!", delete_after=20)

        # await ctx.response.send_message(content='Displaying queue',
        # delete_after=8)

        # for number, track in enumerate(tracks, start=1):

        #     trackDuration = await Utils().durationFormat(track[7])
        #     trackTitle = track[6].replace("*", "\\*")
        #     trackUrl = track[5]

        #     message += f"**{number}) [{trackTitle}]({trackUrl})** ({trackDuration})\n"
        #     if len(message) > 1800:

        #         if isFirstMessage:
        #             embedTitle = "Queue"
        #             isFirstMessage = False
        #         else:
        #             embedTitle = ""

        #         embed=discord.Embed(title=embedTitle, description=message, color=discord.Colour.dark_green())
        #         embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        #         await ctx.channel.send(embed=embed, delete_after=40)
        #         message = ""
        # if len(message) > 0:
        #     embed=discord.Embed(title="", description=message, color=discord.Colour.dark_green())
        #     embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        #     await ctx.channel.send(embed=embed, delete_after=40)

    @discord.slash_command(name="search",
                          description="Search a song on youtube.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def search(self, ctx: discord.Interaction, query: str):
        tracks = await self.bot.wavelink.get_tracks(cls=wavelink.YouTubeMusicTrack, query=f'ytsearch:{query}')

        message = ""
        number = 0
        if tracks is None:
            await noResultFound(self, ctx)
            return None
        for i in tracks:
            if number >= 8:
                break
            number += 1
            duration = await Utils().durationFormat(i.duration)
            message += f"**{number}) [{i.title}]({i.uri}])** ({duration})\n"
        embed = discord.Embed(
            title="Search results :",
            description=f"choose the number that corresponds to the music.\nWrite `0` to pass the cooldown.\n\n{message}",
            color=discord.Colour.dark_green())
        embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        await ctx.response.send_message(embed=embed, delete_after=20)

    @discord.slash_command(name='shuffle',
                          description='Shuffle current queue')
    async def shuffle(self, ctx: discord.Interaction):
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not ctx.user.guild_permissions.administrator:
            if not await Check().userInVoiceChannel(ctx, self.bot):
                return
            if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
                return

        isShuffle = DBServer(
            self.bot.db_connection).displayServer(
            ctx.guild.id)[4]

        if isShuffle == 1:
            DBServer(self.bot.db_connection).updateShuffle(ctx.guild.id, False)
            await ctx.response.send_message(f"{ctx.user.mention} Shuffle disabled!", delete_after=20)
        else:
            DBServer(self.bot.db_connection).updateShuffle(ctx.guild.id, True)
            await ctx.response.send_message(f"{ctx.user.mention} Shuffle enabled!", delete_after=20)

    @discord.slash_command(name='clearqueue',
                          description='Clears the current queue')
    async def clearqueue(self, ctx: discord.Interaction):
        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        DBQueue(self.bot.db_connection).clear(ctx.guild.id)

        await ctx.response.send_message(content=f'{ctx.user.mention} Queue cleared', delete_after=20)


def setup(bot):
    bot.add_cog(viperamusicqueue(bot))
