import discord
import logging
from discord.ext import commands
from viperaveil.utilities.Constants import channels_to_watch
from viperaveil.utilities.database.temp_voice import DBTempVoice

logger = logging.getLogger('discord')

# Intents.voice_states is required!

class ViperaTempVoice(commands.Cog):

    temporary_channels = []
    temporary_categories = []

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')
        for channel in DBTempVoice(self.bot.db_connection).get_all():
            self.temporary_channels.append(int(channel[0]))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        possible_channel_name = f"{member.name}'s room"
        if after.channel:
            if after.channel.id in channels_to_watch:
                temp_channel = await after.channel.clone(name=possible_channel_name)
                await member.move_to(temp_channel)
                self.temporary_channels.append(temp_channel.id)
                DBTempVoice(self.bot.db_connection).add(temp_channel.id, temp_channel.guild.id)
            if after.channel.name == 'teams':
                temporary_category = await after.channel.guild.create_category(name=possible_channel_name)
                await temporary_category.create_text_channel(name="text")
                temp_channel = await temporary_category.create_voice_channel(name="voice")
                await member.move_to(temp_channel)
                self.temporary_categories.append(temp_channel.id)
                DBTempVoice(self.bot.db_connection).add(temp_channel.id, temp_channel.guild.id)

        if before.channel:
            if before.channel.id in self.temporary_channels:
                if len(before.channel.members) == 0:
                    await before.channel.delete()
                    DBTempVoice(self.bot.db_connection).delete(before.channel.id)
            if before.channel.id in self.temporary_categories:
                if len(before.channel.members) == 0:
                    for channel in before.channel.category.channels:
                        await channel.delete()
                        DBTempVoice(self.bot.db_connection).delete(channel.id)
                    await before.channel.category.delete()


def setup(bot):
    bot.add_cog(ViperaTempVoice(bot))
