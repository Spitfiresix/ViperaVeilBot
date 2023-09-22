"""
Connects to lavalink server
Stores variables in self.bot.lavalink
"""
import logging
import wavelink
from wavelink.ext import spotify

from discord.ext import commands

logger = logging.getLogger('discord')


class CogLavalink(commands.Cog):
    """
    Class for constructing wavelink/lavalink
    """

    def __init__(self, bot):
        self.bot = bot

        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    async def start_nodes(self):
        """Starts and connects to Lavalink server"""
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this we will use one server.
        # Region should be a discord.py guild.region e.g sydney
        # or us_central (Though this is not technically required)
        await wavelink.NodePool.create_node(bot=self.bot,
        host=self.bot.lavalink.host,
        port=self.bot.lavalink.port,
        password=self.bot.lavalink.password,
        identifier=self.bot.lavalink.identifier,
        region=self.bot.lavalink.region,
        spotify_client=spotify.SpotifyClient(
        client_id=self.bot.lavalink.spotify_client_id,
        client_secret=self.bot.lavalink.spotify_client_secret))
        self.bot.wavelink = wavelink.NodePool.get_node()


def setup(bot):
    """Imports Cog class on class import"""
    bot.add_cog(CogLavalink(bot))
