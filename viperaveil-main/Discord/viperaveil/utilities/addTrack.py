import datetime
import discord
import wavelink
import json

from viperaveil.utilities.Check import Check
from viperaveil.utilities.Utils import Utils
from viperaveil.utilities.playTrack import playTrack

from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Server import DBServer


async def addTrack(self, ctx: discord.Interaction, tracks):

    if not await Check().userInVoiceChannel(ctx, self.bot):
        return

    # If there is only one track
    if not isinstance(tracks, list):
        tracks = [tracks]

    player: wavelink.Player = ctx.guild.voice_client

    if not player:
        # Clear all the queue
        DBQueue(self.bot.db_connection).clear(ctx.guild.id)

        channel = ctx.user.voice.channel
        player: wavelink.Player = await channel.connect(cls=wavelink.Player)
        await ctx.channel.send(f"{ctx.user.mention} Connected in **`{channel.name}`**!", delete_after=20)

    playlistMessage = None

    for track in tracks:
        tempLink = track
        if isinstance(track, str):
            # Convert the link in a track
            track = await self.bot.wavelink.get_tracks(track)
            track = track[0]
            if track is None:
                return await ctx.channel.send(f"{self.bot.emoji_list.false} The link `{tempLink}` is invalid!", delete_after=20)

        requester = f"{ctx.user.name}#{ctx.user.discriminator}"
        # Add the requester
        if player.is_playing():
            queueSize = DBQueue(
                self.bot.db_connection).countQueueItems(
                ctx.guild.id)
            # if queueSize >= 50:
            #    return await ctx.channel.send(f"{self.bot.emoji_list.false} {ctx.user.mention} You are over the queue limit! The limit of the queue is 50 songs.")
            # Queue sizes can get f**ked!
            index = DBQueue(self.bot.db_connection).getFutureIndex(ctx.guild.id)
            if index is not None:
                index += 1
            else:
                index = 1
            # Add to the queue
            DBQueue(
                self.bot.db_connection).add(
                ctx.guild.id,
                False,
                requester,
                ctx.channel.id,
                ctx.user.voice.channel.id,
                track.uri,
                track.title,
                track.duration,
                track.thumb,
                index)

            trackDuration = await Utils().durationFormat(track.duration)
            trackTitle = track.title.replace("*", "\\*")

            if len(tracks) == 1:

                # Queue size and duration
                queueSizeAndDuration = DBQueue(
                    self.bot.db_connection).queueSizeAndDuration(
                    ctx.guild.id)
                if queueSizeAndDuration:
                    queueDuration = int(queueSizeAndDuration[0])
                    queueDuration = await Utils().durationFormat(queueDuration)
                    queueSize = queueSizeAndDuration[1]
                else:
                    queueSize = 0
                    queueDuration = "00:00"

                embed = discord.Embed(
                    title="Song added to the queue",
                    description=f"New song added : **[{trackTitle}]({track.uri})** ({trackDuration})",
                    color=discord.Colour.dark_green())
                embed.add_field(
                    name="Place in the queue : ",
                    value=f"`{queueSize}`",
                    inline=True)
                embed.add_field(
                    name="Estimated time before playing :",
                    value=f"`{queueDuration}`",
                    inline=True)
                embed.set_thumbnail(url=track.thumb)
                await ctx.channel.send(embed=embed, delete_after=30)
            else:
                # Send message with all tracks added to queue
                multipleTracks = True
                # If it's a playlist => Update the same message to do not spam the channel
                # if playlistMessage is None:
                #     embed=discord.Embed(title="Song added to the queue", description=f"- **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.dark_green())
                #     embed.set_thumbnail(url=track.thumb)
                #     playlistMessage = await ctx.channel.send(embed=embed, delete_after=30)
                # else:
                #     # Update the message
                #     embedEdited = discord.Embed(title="Songs added to the queue", description= playlistMessage.embeds[0].description + f"\n- **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.dark_green())
                #     playlistMessage.embeds[0].description = embedEdited.description
                #     if len(playlistMessage.embeds[0].description) > 1800:
                #         embed=discord.Embed(title="Song added in the queue", description=f"- **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.dark_green())
                #         embed.set_thumbnail(url=track.thumb)
                #         playlistMessage = await ctx.channel.send(embed=embed, delete_after=30)
                #     else:
                # await playlistMessage.edit(embed=embedEdited,
                # delete_after=30)

        else:
            DBServer(
                self.bot.db_connection).clearMusicParameters(
                ctx.guild.id, False, False, False)

            DBQueue(
                self.bot.db_connection).add(
                ctx.guild.id,
                True,
                requester,
                ctx.channel.id,
                ctx.user.voice.channel.id,
                track.uri,
                track.title,
                track.duration,
                track.thumb,
                0)  # Add to the DB
            # Play the track
            await playTrack(self, ctx, player, track, requester)

    await ctx.channel.send(content=f'{len(tracks)} tracks added to the queue', delete_after=20)
