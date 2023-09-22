import discord
from discord.ext import tasks, commands

from viperaveil.utilities.pickup.assistive import isVerified, addQueue
from viperaveil.lib.cogs.vipera.embed import viperaPickupEmbed

_queue = {}

class pickUpEmbedView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.add_item(discord.ui.Button(label='📰 How it works', url="https://discord.com/channels/303245408539246603/1074877620082184284", row=0))

    @discord.ui.button(custom_id='viperaPickUp1v1',
                        label='1v1', style=discord.ButtonStyle.green)
    async def viperaPickUp1v1(self, button: discord.ui.Button, ctx: discord.Interaction):
        verified = isVerified(ctx)
        if not (verified == 'Success'):
            await ctx.response.send_message(content=verified, ephemeral=True, delete_after=20)
            return
        _queue = await addQueue(ctx, '1v1')
        self.bot._queue = _queue
        embed = await viperaPickupEmbed(self, _queue)
        await self.bot.pickup_message.edit(embed=embed, view=pickUpEmbedView(self.bot))

    @discord.ui.button(custom_id='viperaPickUp2v2',
                        label='2v2', style=discord.ButtonStyle.green)
    async def viperaPickUp2v2(self, button: discord.ui.Button, ctx: discord.Interaction):
        verified = isVerified(ctx)
        if not (verified == 'Success'):
            await ctx.response.send_message(content=verified, ephemeral=True, delete_after=20)
            return
        _queue = await addQueue(ctx, '2v2')
        self.bot._queue = _queue
        embed = await viperaPickupEmbed(self, _queue)
        await self.bot.pickup_message.edit(content='',embed=embed, view=pickUpEmbedView(self.bot))

    @discord.ui.button(custom_id='viperaPickUp3v3',
                        label='3v3', style=discord.ButtonStyle.green)
    async def viperaPickUp3v3(self, button: discord.ui.Button, ctx: discord.Interaction):
        verified = isVerified(ctx)
        if not (verified == 'Success'):
            await ctx.response.send_message(content=verified, ephemeral=True, delete_after=20)
            return
        _queue = await addQueue(ctx, '3v3')
        self.bot._queue = _queue
        embed = await viperaPickupEmbed(self, _queue)
        await self.bot.pickup_message.edit(embed=embed, view=pickUpEmbedView(self.bot))

    @discord.ui.button(custom_id='viperaPickUp4v4',
                        label='4v4', style=discord.ButtonStyle.green)
    async def viperaPickUp4v4(self, button: discord.ui.Button, ctx: discord.Interaction):
        verified = isVerified(ctx)
        if not (verified == 'Success'):
            await ctx.response.send_message(content=verified, ephemeral=True, delete_after=20)
            return
        _queue = await addQueue(ctx, '4v4')
        self.bot._queue = _queue
        embed = await viperaPickupEmbed(self, _queue)
        await self.bot.pickup_message.edit(embed=embed, view=pickUpEmbedView(self.bot))