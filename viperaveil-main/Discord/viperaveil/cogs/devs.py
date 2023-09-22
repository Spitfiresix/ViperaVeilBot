"""
Owner commands cog
"""
import logging
import discord
from discord.ext import commands

logger = logging.getLogger('discord')


class Devs(commands.Cog):
    """
    Class for owner only commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @commands.command(name='sync', hidden=True)
    @commands.is_owner()
    async def syncslash(self, ctx: discord.Interaction):
        """Syncs slash commands to all servers"""
        guilds = self.bot.guilds
        for guild in guilds:
            print(f'Syncing slash commands for {guild.name}')
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)
        await ctx.message.delete()
        await ctx.channel.send(content="Slash Commands Sync'd!", delete_after=12)

    @commands.command(name='tidy', hidden=True)
    @commands.is_owner()
    async def clear_self(self, ctx: discord.Interaction):
        """Clears own messages from 'called' channel"""
        def is_self(message):
            return message.author == self.bot.user
        await ctx.message.delete()
        await ctx.channel.purge(check=is_self)

    @commands.command(name='order', hidden=True)
    @commands.is_owner()
    async def clear_all(self, ctx: discord.Interaction, *, order_num: int):
        """Clears all messages from 'called' channel"""
        def is_message(message):
            return True
        if not order_num:
            await ctx.response.send_message(content="You must specify an order m'lord")
            return
        if order_num == 66:
            #await ctx.message.delete()
            await ctx.channel.purge(check=is_message)

    @commands.command(name='log', hidden=True)
    @commands.is_owner()
    async def send_log(self, ctx: discord.Interaction):
        """Responds with current bot log"""
        with open('/app/discord.log') as f:
            file = discord.File(f)
            await ctx.channel.send(file=file, delete_after=20)
        await ctx.message.delete()

    # Hidden means it won't show up on the default help.
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cogmgt_load(self, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        await self.bot.load_extension(cog)

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cogmgt_unload(self, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        await self.bot.unload_extension(cog)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cogmgt_reload(self, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        await self.bot.unload_extension(cog)
        await self.bot.load_extension(cog)

    @commands.command(name='eventloop', hidden=True)
    @commands.is_owner()
    async def event_loop(self, ctx: discord.Interaction):
        await ctx.channel.send(content=f"{self.bot.event_loop_list}", delete_after=12)

def setup(bot):
    """Imports Cog class on module import"""
    bot.add_cog(Devs(bot))
