from viperaveil.utilities.database.Skip import DBSkip
from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Server import DBServer
from viperaveil.utilities.Check import Check
from viperaveil.utilities.addTrack import addTrack
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


async def searchSpotifyTrack(self, ctx: discord.Interaction, args):
    """Get a YouTube link from a Spotify link."""
    await ctx.channel.send(f"{self.bot.emoji_list.spotify_logo} Searching...", delete_after=10)
    # Get track's id
    trackId = tekore.from_url(args)
    try:
        track = await self.bot.spotify.track(trackId[1])
    except BaseException:
        await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.user.mention} The Spotify link is invalid!", delete_after=20)
        return None
    title = track.name
    artist = track.artists[0].name
    # Search on youtube
    track = await self.bot.wavelink.get_tracks(cls=wavelink.YouTubeMusicTrack, query=f'ytsearch:{title} {artist}')
    if len(track) == 0:
        await noResultFound(self, ctx)
        return None
    return track[0]


async def searchSpotifyPlaylist(self, ctx: discord.Interaction, args):
    """Get Spotify links from a playlist link."""
    await ctx.channel.send(f"{self.bot.emoji_list.spotify_logo} Searching...", delete_after=10)
    # Get playlist's id
    playlistId = tekore.from_url(args)
    try:
        playlist = await self.bot.spotify.playlist(playlistId[1])
    except BaseException:
        await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.user.mention} The Spotify playlist is invalid!", delete_after=20)
        return None

    trackLinks = []
    if self.playlistLimit != 0 and playlist.tracks.total > self.playlistLimit:
        await playlistTooLarge(self, ctx)
        return None
    await ctx.channel.send(f"{self.bot.emoji_list.spotify_logo} Loading... (This process can take several seconds)", delete_after=60)
    for i in playlist.tracks.items:
        title = i.track.name
        artist = i.track.artists[0].name
        # Search on youtube
        track = await self.bot.wavelink.get_tracks(cls=wavelink.YouTubeMusicTrack, query=f'ytsearch:{title} {artist}')
        if track is None:
            await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.user.mention} No song found to : `{title} - {artist}` !", delete_after=20)
        else:
            trackLinks.append(track[0])
    if not trackLinks:  # if len(trackLinks) == 0:
        return None
    return trackLinks


async def searchDeezer(self, ctx: discord.Interaction, args):
    """Get a YouTube link from a Deezer link."""
    await ctx.channel.send(f"{self.bot.emoji_list.deezer_logo} Searching...", delete_after=10)
    async with aiohttp.ClientSession() as session:
        async with session.get(args) as response:
            # Chack if it's a track
            if "track" in response._real_url.path:
                link = await searchDeezerTrack(self, ctx, session, response)
                if link is None:
                    return None
                return link
            if "playlist" in response._real_url.path:
                links = await searchDeezerPlaylist(self, ctx, session, response)
                if links is None:
                    return None
                return links
            await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.author.mention} The Deezer link is not a track!", delete_after=20)
            return None


async def searchDeezerTrack(self, ctx: discord.Interaction, session, response):
    # Get the music ID
    trackId = response._real_url.name
    async with session.get(f"https://api.deezer.com/track/{trackId}") as response:
        response = await response.json()
        title = response["title_short"]
        artist = response["artist"]["name"]
        # Search on youtube
        track = await self.bot.wavelink.get_tracks(f'ytsearch:{title} {artist}')
        if len(track) == 0:
            await noResultFound(self, ctx)
            return None
        return track[0]


async def searchDeezerPlaylist(self, ctx: discord.Interaction, session, response):
    # Get the playlist ID
    playlistId = response._real_url.name
    async with session.get(f"https://api.deezer.com/playlist/{playlistId}") as response:
        response = await response.json()
        if self.playlistLimit != 0 and response["nb_tracks"] > self.playlistLimit:
            await playlistTooLarge(self, ctx)
            return None
        await ctx.channel.send(f"{self.bot.emoji_list.deezer_logo} Loading... (This process can take several seconds)", delete_after=60)
        trackLinks = []
        for i in response["tracks"]["data"]:
            title = i["title_short"]
            artist = i["artist"]["name"]
            # Search on youtube
            track = await self.bot.wavelink.get_tracks(f'ytsearch:{title} {artist}')
            if len(track) == 0:
                await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.author.mention} No song found to : `{title} - {artist}` !", delete_after=20)
            else:
                trackLinks.append(track[0])
        if not trackLinks:
            return None
        return trackLinks


async def searchSoundcloud(self, ctx: discord.Interaction, args):
    """Get a YouTube link from a SoundCloud link."""
    await ctx.channel.send(f"{self.bot.emoji_list.soundcloud_logo} Searching...", delete_after=10)

    try:
        ydltrack = await self.bot.soundcloud.resolve(args)
        track = []
    except BaseException:
        pass
    if isinstance(
            ydltrack,
            Playlist):  # track = await self.bot.wavelink.get_tracks(cls=wavelink.SoundCloudTrack,query=args)
        for entries in ydltrack:
            assert isinstance(entries, Track)
            temptrack = await self.bot.wavelink.get_tracks(cls=wavelink.SoundCloudTrack, query=entries.permalink_url)
            if entries.artwork_url:
                temptrack[0].thumb = entries.artwork_url
            else:
                temptrack[0].thumb = 'https://www.viperaveil.net/static/images/soundcloud-icon177.png'
            track.append(temptrack[0])
    else:
        track = await self.bot.wavelink.get_tracks(cls=wavelink.SoundCloudTrack, query=args)
        try:
            track[0].thumb = ydltrack.artwork_url
        except BaseException:
            track[0].thumb = 'https://www.viperaveil.net/static/images/soundcloud-icon177.png'
    if len(track) == 0:
        await noResultFound(self, ctx)
        return None

    elif len(track) > 1:
        if self.playlistLimit != 0 and len(track) > self.playlistLimit:
            await playlistTooLarge(self, ctx)
            return None
        return track  # .tracks
    return track


async def searchQuery(self, ctx: discord.Interaction, args):
    """Get a YouTube link from a query."""
    await ctx.channel.send(f"{self.bot.emoji_list.youtube_logo} Searching...", delete_after=10)

    tracks = await self.bot.wavelink.get_tracks(cls=wavelink.YouTubeMusicTrack, query=f'ytsearch: {args}')

    message = ""
    number = 0
    if tracks is None:
        await noResultFound(self, ctx)
        return None
    for i in tracks[:5]:
        number += 1
        duration = await Utils().durationFormat(i.duration)
        message += f"**{number}) [{i.title}]({i.uri}])** ({duration})\n"
    embed = discord.Embed(
        title="Search results :",
        description=f"choose the number that corresponds to the music.\nWrite `0` to pass the cooldown.\n\n{message}",
        color=discord.Colour.dark_green())
    embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
    await ctx.channel.send(embed=embed, delete_after=20)

    def check(message):
        if message.content.isdigit():
            messageContent = int(message.content)
            if ((messageContent >= 0) and (messageContent <= 5)):
                return message.content
    try:
        msg = await self.bot.wait_for('message', timeout=15.0, check=check)
        if int(msg.content) == 0:
            await ctx.channel.send(f"{ctx.user.mention} Search exit!", delete_after=20)
            await msg.delete()
            return None
        await msg.delete()
        return tracks[int(msg.content) - 1]
    except asyncio.TimeoutError:
        embed = discord.Embed(
            title=f"**TIME IS UP**",
            description=f"{self.bot.emoji_list.false} {ctx.user.mention} You exceeded the response time (15s)",
            color=discord.Colour.red())
        await ctx.channel.send(embed=embed, delete_after=20)
        return None


async def searchPlaylist(self, ctx: discord.Interaction, args):
    """Get YouTube links from a playlist link."""
    await ctx.channel.send(f"{self.bot.emoji_list.youtube_logo} Searching...", delete_after=10)
    videoCount = int(PlaylistsSearch(args, limit=1).result()
                     ["result"][0]["videoCount"])
    if videoCount == 0:
        await noResultFound(self, ctx)
        return None
    if self.playlistLimit != 0 and videoCount > self.playlistLimit:
        await playlistTooLarge(self, ctx)
        return None
    await ctx.channel.send(f"{self.bot.emoji_list.youtube_logo} Loading... (This process can take several seconds)", delete_after=60)
    tracks = await self.bot.wavelink.get_playlist(cls=wavelink.YouTubePlaylist, identifier=args)
    return tracks.tracks


async def playlistTooLarge(self, ctx: discord.Interaction):
    """Send an embed with the error : playlist is too big."""
    embed = discord.Embed(
        title="Search results :",
        description=f"{self.bot.emoji_list.false} The playlist is too big! (max : {self.playlistLimit} tracks)",
        color=discord.Colour.red())
    embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
    await ctx.response.send_message(embed=embed, delete_after=20)


async def noResultFound(self, ctx: discord.Interaction):
    """Send an embed with the error : no result found."""
    embed = discord.Embed(
        title="Search results :",
        description=f"{self.bot.emoji_list.false} No result found!",
        color=discord.Colour.red())
    embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
    await ctx.response.send_message(embed=embed, delete_after=20)


class viperamusiccore(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        if (os.environ.get('DEBUG_MODE') == 'True'):
            with open("viperaveil/configurationtesting.json", "r") as config:
                data = json.load(config)
        else:
            with open("viperaveil/configuration.json", "r") as config:
                data = json.load(config)
        self.playlistLimit = int(data.get("playlistLimit", 15))
        # 0 is nolimit
        print(f"Playlist limit set to {self.playlistLimit}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name="join",
                          description="Add the bot to your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def join(self, ctx: discord.Interaction):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botNotInVoiceChannel(ctx, self.bot):
            return

        channel = ctx.user.voice.channel

        player = await channel.connect(cls=wavelink.Player)
        volume = DBServer(self.bot.db_connection).displayServer(ctx.guild_id)
        await player.set_volume(volume[6])
        # player: wavelink.Player = ctx.voice_client

        # Clear all the queue
        DBQueue(self.bot.db_connection).clear(ctx.guild.id)
        # Clear all server music parameters
        DBServer(
            self.bot.db_connection).clearMusicParameters(
            ctx.guild.id, False, False, False)

        await ctx.response.send_message(f"{ctx.user.mention} Connected to **`{channel.name}`**!", delete_after=20)

    @discord.slash_command(name="leave",
                          description="Leave the bot of your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def leave(self, ctx: discord.Interaction):

        if not await Check().botInVoiceChannel(ctx, self.bot):
            return

        if not ctx.user.guild_permissions.administrator:
            if not await Check().userInVoiceChannel(ctx, self.bot):
                return
            if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
                return

        player: wavelink.Player = ctx.guild.voice_client
        channelId = player.channel.id
        channel = player.channel

        if player.is_playing():
            await player.stop()
        await player.disconnect()
        if hasattr(self.bot, 'lastPlayingSong'):
            try:
                await self.bot.lastPlayingSong.delete()
            except BaseException:
                pass

        # Clear all the queue
        DBQueue(self.bot.db_connection).clear(ctx.guild.id)
        # Clear all server music parameters
        DBServer(
            self.bot.db_connection).clearMusicParameters(
            ctx.guild.id, False, False, False)

        await ctx.response.send_message(f"{ctx.user.mention} Disconnected from **`{channel.name}`**!", delete_after=20)

    @discord.slash_command(name="play",
                          description="The bot searches and plays audio on the url provided.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def play(self, ctx: discord.Interaction, query: str):

        await ctx.response.send_message(content='Processing....', delete_after=5)
        if not await Check().userInVoiceChannel(ctx, self.bot):
            return

        # query = " ".join(query)

        # Spotify
        if query.startswith("https://open.spotify.com"):
            if query.startswith("https://open.spotify.com/track"):
                query = await searchSpotifyTrack(self, ctx, query)
            elif query.startswith("https://open.spotify.com/playlist"):
                query = await searchSpotifyPlaylist(self, ctx, query)
            else:
                return await ctx.channel.send(f"{self.bot.emoji_list.false} {ctx.user.mention} Only Spotify playlists and Spotify tracks are supported!", delete_after=12)
            if query is None:
                return

        # Deezer
        elif query.startswith("https://deezer.page.link") or query.startswith("https://www.deezer.com"):
            query = await searchDeezer(self, ctx, query)
            if query is None:
                return

        # SoundCloud
        elif query.startswith("https://soundcloud.com"):
            query = await searchSoundcloud(self, ctx, query)
            if query is None:
                return

        # Youtube Playlist
        elif query.startswith("https://www.youtube.com/playlist"):
            query = await searchPlaylist(self, ctx, query)
            if query is None:
                return

        # YouTube video
        elif query.startswith("https://www.youtube.com/watch") or query.startswith('https://youtu.be/'):
            await ctx.channel.send(f"{self.bot.emoji_list.youtube_logo} Searching...", delete_after=10)
            if query.__contains__('&list'):
                index = query.find('&list')
                query = query[:index]
            # Check if the link exists
            track = await self.bot.wavelink.get_tracks(cls=wavelink.YouTubeMusicTrack, query=query)
            query = track[0]
            if track is None:
                return await ctx.channel.send(f"{self.bot.emoji_list.false} {ctx.user.mention} The YouTube link is invalid!", delete_after=12)

        # Query
        else:
            query = await searchQuery(self, ctx, query)
            if query is None:
                return

        tracks = query

        await addTrack(self, ctx, tracks)

    @discord.slash_command(name="reload",
                          description="Replay the current song.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def reload(self, ctx: discord.Interaction):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.seek(0)  # Reload the song

        await ctx.response.send_message(f"{ctx.user.mention} Current song reloaded!", delete_after=20)

    @discord.slash_command(name="remove",
                          description="Remove the song with its index.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def remove(self, ctx: discord.Interaction, index: str):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        tracks = DBQueue(self.bot.dbConnection).display(ctx.guild.id)

        if not index.isdigit():
            return await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.user.mention} The index has to be a number!", delete_after=20)
        if (int(index) - 1) > len(tracks):
            return await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.user.mention} The index is invalid!", delete_after=20)

        tracks = DBQueue(self.bot.dbConnection).display(ctx.guild.id)

        if len(tracks) == 0:
            return await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.user.mention} The queue is empty!", delete_after=20)

        index = int(index)
        index = DBQueue(
            self.bot.db_connection).getIndexFromFakeIndex(
            ctx.guild.id, index - 1)

        # Remove
        DBQueue(self.bot.db_connection).remove(ctx.guild.id, index)

        track = tracks[index - 2]
        trackDuration = await Utils().durationFormat(track[7])
        trackTitle = track[6].replace("*", "\\*")
        trackUrl = track[5]

        embed = discord.Embed(
            title="Song Removed from the queue",
            description=f"Song removed : **[{trackTitle}]({trackUrl})** ({trackDuration})",
            color=discord.Colour.dark_green())
        embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        await ctx.response.send_message(embed=embed, delete_after=20)

    @discord.slash_command(name="replay",
                          description="Re-add the last played song to the queue")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def replay(self, ctx: discord.Interaction):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return
        if not await Check().botIsPlaying(ctx, self.bot):
            return

        formerTrack = DBQueue(
            self.bot.db_connection).displayFormer(
            ctx.guild.id)

        if formerTrack is None:
            return await ctx.send(f"{self.bot.emoji_list.false} {ctx.user.mention} There is no former track to replay!", delete_after=20)

        futureIndex = DBQueue(
            self.bot.db_connection).getFutureIndex(
            ctx.guild.id)
        futureIndex += 1

        trackUri = formerTrack[5]
        trackTitle = formerTrack[6].replace("*", "\\*")
        durationInMs = formerTrack[7]
        trackDuration = await Utils().durationFormat(durationInMs)
        requester = f"{ctx.user.name}#{ctx.user.discriminator}"

        # Add the former track at the end of the queue
        DBQueue(
            self.bot.db_connection).add(
            ctx.guild.id,
            False,
            requester,
            ctx.channel.id,
            ctx.guild.voice_client.channel.id,
            trackUri,
            trackTitle,
            durationInMs,
            futureIndex)

        embed = discord.Embed(
            title="Replay",
            description=f"New song added : **[{trackTitle}]({trackUri})** ({trackDuration})",
            color=discord.Colour.dark_green())
        embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        await ctx.response.send_message(embed=embed, delete_after=20)

    @discord.slash_command(name="skip",
                          description="Skip the current song.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def skip(self, ctx: discord.Interaction):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        if not ctx.user.guild_permissions.administrator:

            users = DBSkip(self.bot.db_connection).displayUsers(ctx.guild.id)
            usersCount = len(users)

            # If user had already skip
            if ctx.user.id in [int(i[0]) for i in users]:
                return await ctx.response.send_message(f"{ctx.user.mention} Waiting for other voice users! ({usersCount}/{ceil(len(ctx.user.voice.channel.voice_states)/2)})", delete_after=60)

            else:
                # Add to the DB
                DBSkip(self.bot.db_connection).add(ctx.guild.id, ctx.user.id)
                usersCount += 1

            # Calcul the ratio
            # It's a percentage
            ratio = usersCount / \
                (len(ctx.user.voice.channel.voice_states) - 1) * 100
            if not ratio > 50:
                return await ctx.response.send_message(f"{ctx.user.mention} Waiting for other voice users! ({usersCount}/{ceil(len(ctx.user.voice.channel.voice_states)/2)})", delete_after=60)

        # Clean the dict
        DBSkip(self.bot.db_connection).clear(ctx.guild.id)
        await ctx.response.send_message(f"{ctx.user.mention} Current song skipped!", delete_after=20)

        player: wavelink.Player = ctx.guild.voice_client
        await player.seek(player.track.length * 1000)

    @discord.slash_command(name="volume",
                          description="Change the bot's volume. 0:200")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def volume(self, ctx: discord.Interaction, volume: str):

        if not await Check().userInVoiceChannel(ctx, self.bot):
            return
        if not await Check().botInVoiceChannel(ctx, self.bot):
            return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
            return

        if (
            (not volume.isdigit()) or
            (int(volume)) < 0 or
            (int(volume) > 200)
        ):
            return await ctx.response.send_message(f"{self.bot.emoji_list.false} {ctx.user.mention} The volume has to be a number between 0 and 200!", delete_after=20)

        player: wavelink.Player = ctx.guild.voice_client

        volume = int(volume)
        await player.set_volume(volume)
        DBServer(self.bot.db_connection).updateVolume(ctx.guild.id, volume)

        embed = discord.Embed(
            title="Volume changed :",
            description=f"Volume changed to : ``{volume} %``",
            color=discord.Colour.dark_green())
        embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        await ctx.response.send_message(embed=embed, delete_after=20)


def setup(bot):
    bot.add_cog(viperamusiccore(bot))
