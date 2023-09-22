"""
Vipera Account sync cog
"""
import logging
import discord
from discord.ext import commands
from viperaveil.lib.cogs.rsi.link import RSILink
from viperaveil.utilities.Constants import ORG_ROLE_MAPPING

logger = logging.getLogger('discord')


class ViperaAuth(commands.Cog):
    """
    Class for Vipera account syncing
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name='link',
                          description='Link your RSI account to Discord')
    async def link(self, ctx, scusername: discord.Option(str, name='rsi-username',description='Enter your RSI username', default = None)):
        """Syncing Discord and RSI accounts"""
        status = await RSILink(self.bot, ctx, scusername)
        debug_channel = ctx.guild.get_channel(435861929844801536)
        await debug_channel.send(content=f'RSI Verification: {ctx.user.name} {status[0]} {status[1]}')
        if ctx.guild.id == 303245408539246603:
            if status[0] == 'verified':
                if status[1]:
                    org_present = False
                    viperaveil_guild: discord.Guild = self.bot.get_guild(303245408539246603)
                    member: discord.Member = await viperaveil_guild.fetch_member(ctx.user.id)
                    for org in ORG_ROLE_MAPPING:
                        if org[1] == status[1]:
                            org_role = viperaveil_guild.get_role(org[0])
                            if not org[0] in member.roles:
                                await ctx.user.add_roles(org_role)
                            org_present = True
                    if not org_present:
                        await ctx.edit_original_response(content=f"Your org doesn't appear to be present in this server, if you would like it added then please contact {viperaveil_guild.get_member(161612500981252096).mention}, {viperaveil_guild.get_member(197435849498034177).mention} or {viperaveil_guild.get_member(316296425149431809).mention}")



def setup(bot):
    """Imports Cog class on module import"""
    bot.add_cog(ViperaAuth(bot))
