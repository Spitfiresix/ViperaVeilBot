"""
TopGG Sync cog
"""
import logging
#import topgg
from discord.ext import commands

logger = logging.getLogger('discord')


class TopGG(commands.Cog):
    """
    Class for TopGG API Sync
    """
    def __init__(self, bot):
        self.bot = bot
        self.token = self.bot.dbl_token
        # self.dblpy = topgg.DBLClient(
            # self.bot, self.token, autopost=True
            # Autopost will post your guild count every 30 minutes
            # webhook_path=bot.dblWebhookPath, webhook_auth=bot.dblWebhookAuth
        # )

    # @commands.Cog.listener()
    # async def on_guild_post(self):
    #     print("Server count posted successfully")

    # @commands.Cog.listener()
    # async def on_dbl_vote(data):
    #     print("New vote", data)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')


def setup(bot):
    """Imports Cog class on module import"""
    bot.add_cog(TopGG(bot))
