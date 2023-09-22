import discord
from discord import Interaction
from discord.ext import commands
from viperaveil.lib.cogs.rsi.lookup import RSILookup
import logging
logger = logging.getLogger('discord')


class viperaplayer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name='rsi',
                          description='Prints specified RSI user info')
    @discord.option(name='rsi_username', description='Enter the RSI handle to search')
    async def rsi(self, ctx: Interaction, scusername: str):
        await RSILookup(self, ctx, scusername)

    @discord.slash_command(name='ping', description='Ping user')
    async def pingUser(self, ctx: discord.Interaction, member: discord.Option(discord.Member, "@Discord User")):
        if 1000868850960715931 in [discRole.id for discRole in ctx.user.roles]:
            await ctx.channel.send(member.mention)
        else:
            await ctx.response.send_message(content="You don't have access to run this command!", ephemeral=True, delete_after=12)


def setup(bot):
    bot.add_cog(viperaplayer(bot))
