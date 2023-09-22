import discord

from discord import ui, Interaction
from discord.ext import commands
from datetime import datetime
from viperaveil.lib.cogs.vipera.embed import viperaEventLeaderboard

import logging
logger = logging.getLogger('discord')

class eventdetails(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = 'Event Details'
        self.add_item(
            label='Event Name',
            style=discord.InputTextStyle.short,
            placeholder="Event Name",
            required=True)
        self.add_item(
            label='Event Icon',
            style=discord.InputTextStyle.short,
            placeholder="url - https://robertsspaceindustries.com/media/eonii7j69hljqr/heap_infobox/SNEK-Logo.png",
            required=False)
        self.add_item(
            label='Date/Time',
            style=discord.InputTextStyle.short,
            placeholder="01/01/2000",
            required=False)
        self.add_item(
            label='Participating Orgs',
            style=discord.InputTextStyle.short,
            placeholder="Vipera Veil, R4M...etc",
            required=False)
        self.add_item(
            label='Event Webpage',
            style=discord.InputTextStyle.short,
            placeholder="url - https://www.daymarrally.com/",
            required=False)

    async def callback(self, ctx: Interaction):
        embed = discord.Embed(
            title=self.title,
            description=f"**{self.children[0].label}**\n{self.children[0]}\n \n \n**{self.children[1].label}**\n{self.children[1]}\n \n \n**{self.children[2].label}**\n{self.children[2]}\n \n \n**{self.children[3].label}**\n{self.children[3]}\n \n \n**{self.children[4].label}**\n{self.children[4]}",
            timestamp=datetime.now(),
            colour=discord.Colour.green())
        embed.set_author(
            name=ctx.user,
            icon_url=ctx.user.avatar)
        await ctx.response.send_message(embed=embed)


class viperaorgevents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name='eventresults',
                          description='Enter the event details for leaderboard')
    # @app_commands.rename(scusername='rsi_username')
    # @app_commands.describe(scusername='Enter your RSI username')
    async def eventresults(ctx, interactions: Interaction):
        await interactions.response.send_modal(eventdetails())

    @discord.slash_command(name='eventleaderboard',
                          description='Enter the event details for leaderboard')
    async def eventleaderboard(ctx, interactions: Interaction):
        if interactions.channel_id == 1048408325152317470:
            detailsEmbed = viperaEventLeaderboard()
            await interactions.channel.send(embed=detailsEmbed)


def setup(bot):
    bot.add_cog(viperaorgevents(bot))
