import discord
import wavelink
from math import ceil

from viperaveil.utilities.Check import Check

from viperaveil.utilities.database.Skip import DBSkip
from viperaveil.utilities.database.Server import DBServer


async def skip(self, ctx: discord.Interaction):

    if not await Check().userInVoiceChannel(ctx, self.bot):
        return
    if not await Check().botInVoiceChannel(ctx, self.bot):
        return
    if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
        return
    user_role_ids = []
    for role in ctx.user.roles:
        user_role_ids.append(role.id)
    if not 1078991468506652723 in user_role_ids and not ctx.user.guild_permissions.administrator: #and not ctx.user.id == 316296425149431809:

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


async def reload(self, ctx: discord.Interaction):

    if not await Check().userInVoiceChannel(ctx, self.bot):
        return
    if not await Check().botInVoiceChannel(ctx, self.bot):
        return
    if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
        return

    player: wavelink.Player = ctx.guild.voice_client
    await player.seek(0)  # Reload the song

    # send_message(f"{ctx.user.mention} Current song reloaded!", delete_after=0)
    await ctx.response.defer()


async def resume(self, ctx: discord.Interaction):

    if not await Check().userInVoiceChannel(ctx, self.bot):
        return
    if not await Check().botInVoiceChannel(ctx, self.bot):
        return
    if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
        return

    player: wavelink.Player = ctx.guild.voice_client

    if player:
        if not player.is_playing():
            return await ctx.response.send_message(f"{ctx.user.mention} No song is currently playing!", delete_after=20)
    if player.is_paused:
        await player.set_pause(False)
        # .send_message(f"{ctx.user.mention} The song is resumed!", delete_after=0)
        return await ctx.response.defer()
    await ctx.response.send_message(f"{ctx.user.mention} The song is already resumed!", delete_after=0)


async def pause(self, ctx: discord.Interaction):

    if not await Check().userInVoiceChannel(ctx, self.bot):
        return
    if not await Check().botInVoiceChannel(ctx, self.bot):
        return
    if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
        return

    player: wavelink.Player = ctx.guild.voice_client
    if player:
        if not player.is_playing():
            return await ctx.response.send_message(f"{ctx.user.mention} No song is currently playing!", delete_after=0)
    if not player.is_paused():
        await player.set_pause(True)
        # .send_message(f"{ctx.user.mention} The song is paused!", delete_after=0)
        return await ctx.response.defer()
    await ctx.response.send_message(f"{ctx.user.mention} The song is already paused!", delete_after=0)


async def loop(self, ctx: discord.Interaction):

    if not await Check().userInVoiceChannel(ctx, self.bot):
        return
    if not await Check().botInVoiceChannel(ctx, self.bot):
        return
    if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
        return

    isLoop = DBServer(self.bot.db_connection).displayServer(ctx.guild.id)[2]

    if isLoop == 1:
        DBServer(self.bot.db_connection).updateLoop(ctx.guild.id, False)
        # .send_message(f"{ctx.user.mention} Single loop mode disabled!", delete_after=0)
        await ctx.response.defer()
    else:
        DBServer(self.bot.db_connection).updateLoop(ctx.guild.id, True)
        # .send_message(f"{ctx.user.mention} Single loop mode enabled!", delete_after=0)
        await ctx.response.defer()


async def loopqueue(self, ctx: discord.Interaction):

    if not await Check().userInVoiceChannel(ctx, self.bot):
        return
    if not await Check().botInVoiceChannel(ctx, self.bot):
        return
    if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
        return

    isLoopQueue = DBServer(
        self.bot.db_connection).displayServer(
        ctx.guild.id)[3]

    if isLoopQueue == 1:
        DBServer(self.bot.db_connection).updateLoopQueue(ctx.guild.id, False)
        # .send_message(f"{ctx.user.mention} Queue looping mode disabled!", delete_after=0)
        await ctx.response.defer()
    else:
        DBServer(self.bot.db_connection).updateLoopQueue(ctx.guild.id, True)
        # .send_message(f"{ctx.user.mention} Queue looping mode enabled!", delete_after=0)
        await ctx.response.defer()


async def shuffle(self, ctx: discord.Interaction):

    if not await Check().userInVoiceChannel(ctx, self.bot):
        return
    if not await Check().botInVoiceChannel(ctx, self.bot):
        return
    if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot):
        return

    isShuffle = DBServer(self.bot.db_connection).displayServer(ctx.guild.id)[4]

    if isShuffle == 1:
        DBServer(self.bot.db_connection).updateShuffle(ctx.guild.id, False)
        # .send_message(f"{ctx.user.mention} Queue looping mode disabled!", delete_after=0)
        await ctx.response.defer()
    else:
        DBServer(self.bot.db_connection).updateShuffle(ctx.guild.id, True)
        # .send_message(f"{ctx.user.mention} Queue looping mode enabled!", delete_after=0)
        await ctx.response.defer()
