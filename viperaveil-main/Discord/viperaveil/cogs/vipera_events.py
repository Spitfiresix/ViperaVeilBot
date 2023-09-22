"""
Vipera Events listener cog
"""
import logging
from datetime import datetime
import wavelink
import discord
from discord import ui, Interaction
from discord.ext import commands
from viperaveil.utilities.database.Queue import DBQueue
from viperaveil.utilities.database.Server import DBServer

logger = logging.getLogger('discord')

class EventDetails(ui.Modal):
    """Class for custom event line modal"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
        label='Event Name',
        style=discord.InputTextStyle.short,
        placeholder="Event Name",
        required=True))
        self.add_item(ui.InputText(
        label='Event Date/Time',
        style=discord.InputTextStyle.short,
        placeholder="20/12/2023 16:00",
        required=True))


    async def callback(self, ctx: Interaction): # pylint: disable=arguments-differ
        """Called on modal submit"""
        try:
            event_timestamp = int(
                (datetime.strptime(
                    self.children[1].value,
                    '%d/%m/%Y %H:%M')).timestamp())
            event_data = f'Date: <t:{event_timestamp}:F> From Now: <t:{event_timestamp}:R>'
        except BaseException: # pylint: disable=bare-except,broad-except
            await ctx.response.send_message(
                content='DateTime needs to be in format 20/12/2023 16:00!',
                ephemeral=True, delete_after=20)
            return
        embed = discord.Embed(
            title=self.children[0].value,
            description=event_data,
            timestamp=datetime.now(),
            colour=discord.Colour.dark_green())
        embed.set_footer(text=ctx.user, icon_url=ctx.user.avatar)
        await ctx.response.defer()
        await ctx.channel.send(embed=embed)


class ViperaEvents(commands.Cog):
    """
    Class for Vipera Events listener
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Calls on user voice state change"""
        # If the bot leave a voice channel
        if (before.channel is not None) and (after.channel is None):
            if member == self.bot.user:

                player: wavelink.Player = before.channel.guild.voice_client
                if player:
                    if player.is_playing():
                        await player.disconnect()
                DBQueue(self.bot.db_connection).clear(before.channel.guild.id)
                DBServer(self.bot.db_connection).clearMusicParameters(
                    before.channel.guild.id, False, False, False)

        if (before.channel is not None) and (
                after.channel is not before.channel):
            if (
                (self.bot.user.id in before.channel.voice_states.keys() and
                 len(before.channel.voice_states) == 1)
                or
                (member == self.bot.user)
            ):
                if member != self.bot.user:
                    player: wavelink.Player = before.channel.guild.voice_client
                    await player.disconnect()
                try:
                    await self.bot.lastPlayingSong.delete()
                except BaseException: # pylint: disable=bare-except,broad-except
                    pass

                DBServer(self.bot.db_connection).clearMusicParameters(
                    before.channel.guild.id, False, False, False)

        # If the bot join a voice channel
        elif (before.channel is None) and (after.channel is not None):
            if member == self.bot.user:

                DBServer(
                    self.bot.db_connection).clearMusicParameters(
                    after.channel.guild.id, False, False, False)

    @discord.slash_command(name='datetime',
                          description='Display message with timestamp after')
    async def viperadatetime(self, ctx: discord.Interaction):
        """Calls modal defined above"""
        await ctx.response.send_modal(EventDetails(title='Example Modal'))


def setup(bot):
    """Imports Cog class on module import"""
    bot.add_cog(ViperaEvents(bot))
