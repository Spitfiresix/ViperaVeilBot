import discord
import asyncio
from discord.ext import commands
import logging
from viperaveil.utilities.Constants import snekLogoRegular
from viperaveil.lib.cogs.vipera.embed import vipera_ticket
logger = logging.getLogger('discord')


class TicketEmbedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id='TicketEmbedViewPilot',
                       label='Flight School',
                       emoji='🚀',
                       style=discord.ButtonStyle.green)
    async def rsiLink(self, button: discord.ui.Button, ctx: discord.Interaction):
        channels = await ctx.guild.fetch_channels()
        selfchannelexists = None
        channellist = ''
        for channel in channels:
            channellist = (channellist + f'{channel.name}\n')
            if ctx.user.name.lower() in channel.name:
                selfchannelexists = True
                trainingchannel = channel
        if not selfchannelexists:
            await viperaticket.ticketCreate(self, ctx, tickettype='pilot')
        else:
            await ctx.response.send_message(embed=discord.Embed(description=f'You already have a training channel - {trainingchannel.mention}, note that you can only request 1 type of training at a time.', colour=discord.Colour.red()), ephemeral=True, delete_after=12)

    @discord.ui.button(custom_id='TicketEmbedViewFPS',
                       label='FPS School',
                       emoji='🔫',
                       style=discord.ButtonStyle.blurple)
    async def rsiButton(self, button: discord.ui.Button, ctx: discord.Interaction):
        channels = await ctx.guild.fetch_channels()
        selfchannelexists = None
        channellist = ''
        for channel in channels:
            channellist = (channellist + f'{channel.name}\n')
            if ctx.user.name.lower() in channel.name:
                selfchannelexists = True
                trainingchannel = channel
        if not selfchannelexists:
            await viperaticket.ticketCreate(self, ctx, tickettype='fps')
        else:
            await ctx.response.send_message(embed=discord.Embed(description=f'You already have a training channel - {trainingchannel.mention}, note that you can only request 1 type of training at a time.', colour=discord.Colour.red()), ephemeral=True, delete_after=12)


class OpenTicketEmbedView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id='OpenTicketEmbedViewAccept',
                       label='Accept', emoji='✅', style=discord.ButtonStyle.grey, disabled=True)
    async def AcceptTicket(self, button: discord.ui.Button, ctx: discord.Interaction):
        await ctx.response.send_message(embed=discord.Embed(description='Not currently in use', colour=discord.Colour.red()), ephemeral=True, delete_after=12)

    @discord.ui.button(custom_id='OpenTicketEmbedViewClose',
                       label='Close', emoji='🔒', style=discord.ButtonStyle.grey)
    async def CloseTicket(self, button: discord.ui.Button, ctx: discord.Interaction):
        await ctx.response.send_message(embed=discord.Embed(description='Closing ticket'), ephemeral=True, delete_after=4)
        i = 9
        message = await ctx.channel.send(embed=discord.Embed(description=f'Ticket closed by {ctx.user}, deleting in 10 second(s)', colour=discord.Colour.orange()))
        while i > 0:
            newEmbed = discord.Embed(
                description=f'Ticket closed by {ctx.user.mention}, deleting in {i} second(s)',
                colour=discord.Colour.orange())
            await message.edit(embed=newEmbed)
            await asyncio.sleep(1)
            i -= 1
        await ctx.channel.delete()


class viperaticket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name='ticketcontrol')
    async def ticket(self, ctx: discord.Interaction):
        if ctx.user.id in [161612500981252096,316296425149431809]:
            embed = vipera_ticket(self)
            await ctx.channel.send(embed=embed, view=TicketEmbedView())
            await ctx.response.send_message(embed=discord.Embed(title='Created Embed'), ephemeral=True, delete_after=6)
        else:
            await ctx.response.send_message(embed=discord.Embed(title="You don't have access to run this command", colour=discord.Colour.red()), ephemeral=True, delete_after=12)

    # Instructor Roles
    fps_instructor_role = 1048437819221217320
    pilot_instructor_role = 1016615096824377414

    async def ticketCreate(self, ctx: discord.Interaction, tickettype: str):
        fpsrole: discord.Role = ctx.guild.get_role(
            viperaticket.fps_instructor_role)
        pilotrole: discord.Role = ctx.guild.get_role(
            viperaticket.pilot_instructor_role)
        council: discord.Role = ctx.guild.get_role(1000868850960715931)
        training_category = discord.utils.get(ctx.guild.categories, id=1100349788756656158)
        if tickettype == 'fps':
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.user: discord.PermissionOverwrite(read_messages=True),
                fpsrole: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                council: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
            roleping: discord.Role = fpsrole
            channel = await ctx.guild.create_text_channel(name=f'{tickettype}-{ctx.user.name}', overwrites=overwrites, category=training_category)
        elif tickettype == 'pilot':
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(
                    read_messages=False), ctx.user: discord.PermissionOverwrite(
                    read_messages=True), pilotrole: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True), council: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True)}
            roleping: discord.Role = pilotrole
            channel = await ctx.guild.create_text_channel(name=f'{tickettype}-{ctx.user.name}', overwrites=overwrites, category=training_category)
        else:
            ctx.response.send_message(
                embed=discord.Embed(
                    title='An error occured...',
                    color=discord.Colour.red()),
                ephemeral=True,
                delete_after=12)
            return
        await channel.send(content=roleping.mention)
        await channel.send(embed=discord.Embed(title='Request raised', description=f'Instructors will be with you shortly.', colour=discord.Colour.dark_green()), view=OpenTicketEmbedView())
        await ctx.response.send_message(embed=discord.Embed(description=f'Ticket Created! {channel.mention}'), ephemeral=True, delete_after=30)

    # async def ticketAssign(self, ctx: discord.Interaction):
    #     if self.ticket_creator == user_id:

    #         embed = discord.Embed(
    #             title = "You cant claim the ticket!",
    #             color = 0x0000ff)
    #         embed.set_author(name="TiLiKas Ticket Bot")

    #         await channel.send(embed=embed)

    #     else:

    #         embed = discord.Embed(
    #             title = "Ticket claimed!",
    #             description = f"The ticket was claimed by {user.mention}.",
    #             color = 0x0000ff)
    #         embed.set_author(name="TiLiKas Ticket Bot")

    #         await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(viperaticket(bot))
