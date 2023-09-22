import discord
import json

from discord import ui, Interaction
from discord.ext import commands

from youtubesearchpython import Video, ResultMode

from viperaveil.utilities.database.Playlist import DBPlaylist

from viperaveil.utilities.addTrack import addTrack

import logging
logger = logging.getLogger('discord')


class viperamusicplaylist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @commands.group(name="playlist", invoke_without_command=True)
    async def playlist(self, ctx: discord.Interaction):
        pass

    @playlist.command(name="add",
                      description="Add a song to your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def playlist_add(self, ctx: discord.Interaction, link: str):
        if not link.startswith("https://www.youtube.com/watch"):
            return await ctx.response.send_message(f"{self.bot.emojiList.false} {ctx.user.mention} The YouTube link is invalid!", delete_after=20)
        # Check if the link exists
        track = await self.bot.wavelink.get_tracks(link)
        track = track[0]
        if track is None:
            return await ctx.response.send_message(f"{self.bot.emojiList.false} {ctx.user.mention} The YouTube link is invalid!", delete_after=20)

        playlistSize = DBPlaylist(
            self.bot.db_connection).countPlaylistItems(
            ctx.author.id, "liked")  # Request
        if playlistSize >= 25:
            return await ctx.response.send_message(f"{self.bot.emojiList.false} {ctx.user.mention} Your playlist (liked) is full (25 songs)!", delete_after=20)
        DBPlaylist(
            self.bot.db_connection).add(
            ctx.user.id,
            "liked",
            track.title,
            track.uri)  # Request

        embed = discord.Embed(
            title="Song added in your playlist",
            description=f"- **[{track.title}]({track.uri})**",
            color=discord.Colour.dark_green())
        embed.add_field(name="playlist name :", value=f"`liked`", inline=True)
        embed.add_field(
            name="playlist size :",
            value=f"`{playlistSize+1}/25`",
            inline=True)
        embed.set_thumbnail(url=track.thumb)
        embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        await ctx.channel.send(embed=embed, delete_after=40)

    @playlist.command(name="show",
                      description="Show your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def playlist_show(self, ctx: discord.Interaction):
        playlistContent = DBPlaylist(
            self.bot.db_connection).display(
            ctx.user.id,
            "liked")  # Request

        if len(playlistContent) <= 0:
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.user.mention} Your playlist (liked) is empty!", delete_after=20)

        isFirstMessage = True
        message = ""
        for number, i in enumerate(playlistContent, start=1):
            message += f"**{number}) [{i[2]}]({i[3]})**\n"
            if len(message) > 1800:

                if isFirstMessage:
                    embedTitle = "Liked Playlist :"
                    isFirstMessage = False
                else:
                    embedTitle = ""

                embed = discord.Embed(
                    title=embedTitle,
                    description=message,
                    color=discord.Colour.dark_green())
                embed.set_footer(
                    text=ctx.user.name,
                    icon_url=ctx.user.display_avatar)
                await ctx.response.send_message(embed=embed, delete_after=40)
                message = ""
        if len(message) > 0:
            embedTitle = "Liked Playlist :" if isFirstMessage else ""

            embed = discord.Embed(
                title=embedTitle,
                description=message,
                color=discord.Colour.dark_green())
            embed.set_footer(
                text=ctx.user.name,
                icon_url=ctx.user.display_avatar)
            await ctx.response.send_message(embed=embed, delete_after=40)

    @playlist.command(name="remove",
                      description="Remove a song of your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def playlist_remove(self, ctx: discord.Interaction, index: str):

        index = int(index) - 1

        playlistContent = DBPlaylist(
            self.bot.db_connection).display(
            ctx.user.id,
            "liked")  # Request
        if len(playlistContent) <= 0:
            return await ctx.response.send_message(f"{self.bot.emojiList.false} {ctx.user.mention} Your playlist (liked) is empty!", delete_after=20)

        if index < 0 or index > (len(playlistContent) - 1):
            return await ctx.response.send_message(f"{self.bot.emojiList.false} {ctx.user.mention} The index is unavailable!", delete_after=20)
        DBPlaylist(
            self.bot.db_connection).remove(
            ctx.user.id,
            "liked",
            playlistContent[index][3])  # Request

        embed = discord.Embed(
            title="Song removed from your playlist (liked)",
            description=f"- **[" +
            playlistContent[index][2] +
            "](" +
            playlistContent[index][3] +
            ")**",
            color=discord.Colour.dark_green())
        embed.set_footer(text=ctx.user.name, icon_url=ctx.user.display_avatar)
        await ctx.response.send_message(embed=embed, delete_after=20)

    @playlist.command(name="load",
                      description="Load all songs of your playlist in the queue")
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def playlist_load(self, ctx: discord.Interaction):

        playlistContent = DBPlaylist(
            self.bot.db_connection).display(
            ctx.user.id,
            "liked")  # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.user.mention} Your playlist (liked) is empty!", delete_after=20)

        links = [i[3] for i in playlistContent]
        await addTrack(self, ctx, links)


def setup(bot):
    bot.add_cog(viperamusicplaylist(bot))
