import discord
import wavelink


class Check:

    async def userInVoiceChannel(self, ctx: discord.Interaction, bot):
        """Check if the user is in a voice channel"""
        if ctx.user.voice:
            return True
        await ctx.response.send_message(f"{bot.emoji_list.false} {ctx.user.mention} You are not connected in a voice channel!", delete_after=20)
        return False

    async def botInVoiceChannel(self, ctx: discord.Interaction, bot):
        """Check if the bot is in a voice channel"""
        player: wavelink.Player = ctx.guild.voice_client

        if player:
            return True
        await ctx.response.send_message(f"{bot.emoji_list.false} {ctx.user.mention} I'm not connected in a voice channel!", delete_after=20)
        return False

    async def botNotInVoiceChannel(self, ctx: discord.Interaction, bot):
        """Check if the bot is not in a voice channel"""
        player: wavelink.Player = ctx.guild.voice_client

        if not player:
            return True
        await ctx.response.send_message(f"{bot.emoji_list.false} {ctx.user.mention} I'm already connected in a voice channel!", delete_after=20)
        return False

    async def userAndBotInSameVoiceChannel(self, ctx: discord.Interaction, bot):
        """Check if the user and the bot are in the same voice channel"""
        player: wavelink.Player = ctx.guild.voice_client

        if (
            (bot.user.id in ctx.user.voice.channel.voice_states) and
            (ctx.user.id in ctx.user.voice.channel.voice_states)
        ):
            return True
        await ctx.response.send_message(f"{bot.emoji_list.false} {ctx.user.mention} You are not connected in the same voice channel that the bot!", delete_after=20)
        return False

    async def botIsPlaying(self, ctx: discord.Interaction, bot):
        """Check if the bot is playing"""
        player: wavelink.Player = ctx.guild.voice_client

        if player.is_playing:
            return True
        await ctx.response.send_message(f"{bot.emoji_list.false} {ctx.user.mention} There is currently no song to replay!", delete_after=20)
        return False
