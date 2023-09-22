import discord
import psutil
import platform

from datetime import datetime

from discord.ext import commands
from discord import Interaction

from viperaveil.utilities.database.Queue import DBQueue

import logging
logger = logging.getLogger('discord')


class viperastats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name="stats",
                          description="Display the bot's stats")
    @commands.cooldown(1, 5)
    async def stats(self, ctx: discord.Interaction):

        serverCount = len(self.bot.guilds)
        try:
            userCount = sum(i.member_count for i in self.bot.guilds)
        except BaseException:
            userCount = None
        try:
            viperawlink = self.bot.wavelink.identifier
        except BaseException:
            viperawlink = 'None'
        playingServerCount = DBQueue(self.bot.db_connection).countPlayingItems()

        embed = discord.Embed(
            title=f"{self.bot.user.name}'s Stats",
            description="[**Support**](discordLink)",
            color=discord.Colour.dark_green(),
            timestamp=datetime.now())
        embed.set_thumbnail(url=f'{self.bot.user.display_avatar}')
        embed.add_field(
            name="Statistics :",
            value=f"` Servers : {serverCount} \n Users : {userCount} `",
            inline=True)
        embed.add_field(
            name="Using :",
            value=f"` Python : v{platform.python_version()} \n Module : v{discord.__version__} `",
            inline=True)
        embed.add_field(
            name="RAM :",
            value=f"` Used : {psutil.virtual_memory().percent}% `",
            inline=True)
        embed.add_field(
            name="Music :",
            value=f"Playing music on `{playingServerCount}` server(s)",
            inline=False)
        embed.add_field(
            name='Platform',
            value=f'{platform.system()}',
            inline=True)
        embed.add_field(
            name='Lavalink',
            value=f'Connected Nodes: `{viperawlink}`',
            inline=True)
        latency = int(self.bot.latency * 1000)
        embed.set_footer(text=f"{latency}ms", icon_url=ctx.user.display_avatar)
        await ctx.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(viperastats(bot))
