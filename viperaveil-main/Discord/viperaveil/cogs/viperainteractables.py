import discord
from discord import ui, Interaction
from discord.ext import commands
# from viperaveil.lib.views.viperasplash import RSILink, RSILookup
from viperaveil.lib.cogs.rsi.lookup import RSILookup
from viperaveil.lib.cogs.rsi.link import RSILink
from viperaveil.utilities.Constants import snekLogoRegular, rsiLogo, ORG_ROLE_MAPPING
import logging
logger = logging.getLogger('discord')

embed = discord.Embed(
    title='Vipera Veil',
    description='RSI Verification, Lookup and Event Tool.\nDeveloped and maintained by Vipera Veil',
    url='<discord link>',
    colour=discord.Colour.dark_green())
embed.set_author(name='SNEK')
embed.set_thumbnail(url=snekLogoRegular)
embed.add_field(
    name='RSI Lookup',
    value='Displays information about a given users RSI account, this also works for Discord accounts',
    inline=False)
embed.add_field(
    name='RSI Link',
    value="""Link your RSI account with your Discord account.
    This will allow you to take part in events, and play the Vipera RPG""",
    inline=False
)


class viperainteractables(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    class rsiLookupModal(ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.title = 'RSI Lookup'

            self.add_item(ui.InputText(label='RSI Handle',
            style=discord.InputTextStyle.short,
            placeholder="RSI Handle To Seach For",
            required=True))

        async def callback(self, ctx: Interaction):
            await RSILookup(self, ctx, self.children[0].value, auto_delete=True)

    class rsiLinkModal(ui.Modal):
        def __init__(self, bot, session, *args, **kwargs) -> None:
            self.bot = bot
            self.session = session
            super().__init__(*args, **kwargs)
            self.title = 'RSI Link'

            self.add_item(ui.InputText(
            label='RSI Handle',
            style=discord.InputTextStyle.short,
            placeholder="Your RSI Handle",
            required=True))

        async def callback(self, ctx: Interaction):
            status = await RSILink(self, ctx, self.children[0].value)
            if not status:
                status = ('Not','Found')
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
                                    await member.add_roles(org_role)
                                org_present = True
                        if not org_present:
                            await ctx.edit_original_response(content=f"Your org doesn't appear to be present in this server, if you would like it added then please contact {viperaveil_guild.get_member(161612500981252096).mention}, {viperaveil_guild.get_member(197435849498034177).mention} or {viperaveil_guild.get_member(316296425149431809).mention}")

    class EmbedView(discord.ui.View):
        def __init__(self, bot, session):
            super().__init__(timeout=None)
            self.bot = bot
            self.session = session
            self.add_item(
                discord.ui.Button(
                    label='Join the Orgs!',
                    emoji='<:SNEK:1038010133072052245>',
                    url='https://discord.com/channels/303245408539246603/995852958304583870'))

        @discord.ui.button(custom_id='EmbedViewRSIButton',
                           label='RSI Lookup',
                           emoji='<:MonkaThink:896698581585653800>',
                           style=discord.ButtonStyle.green)
        async def rsiButton(self, button: discord.ui.Button, ctx: discord.Interaction):
            await ctx.response.send_modal(viperainteractables.rsiLookupModal(title='RSI Lookup'))

        @discord.ui.button(custom_id='EmbedViewRSILink',
                           label='RSI Link',
                           emoji='➕',
                           style=discord.ButtonStyle.blurple)
        async def rsiLink(self, button: discord.ui.Button, ctx: discord.Interaction):
            await ctx.response.send_modal(viperainteractables.rsiLinkModal(self.bot, self.session, title='RSI Link'))

    @discord.slash_command(name="viperaintro")
    async def viperaintro(self, ctx: discord.Interaction):
        if ctx.user.id in [316296425149431809, 161612500981252096, 197435849498034177]:
            await ctx.response.send_message(content='Sending embed', ephemeral=True, delete_after=12)
            await ctx.channel.send(embed=embed, view=viperainteractables.EmbedView(self.bot, self.bot.session))
            return
        else:
            await ctx.response.send_message(content="You don't have access to run this command", ephemeral=True, delete_after=12)
            return

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     """Command to send embed with contextual commands for Vipera Veil"""
        # guild_id: discord.Guild.id = 303245408539246603
        # channel_id: discord.TextChannel.id = 1018444002883797013 #'941634559274016778' <- look-up-citizen
        # channel: discord.TextChannel = self.bot.get_guild(guild_id).get_channel(channel_id)
        # #EmbedView.add_item(self, item=discord.ui.Button(label='Join the Org!', url='https://discord.com/channels/303245408539246603/995852958304583870', style=discord.ButtonStyle.url))
        # #role = discord.utils.get(channel.guild.roles, name='RSI Verified')
        # def is_starter(message):
        #     if message.author == self.bot.user:
        #         return True
        #     return False

        # await channel.purge(check=is_starter)

        # self.message: discord.message = await channel.send(embed=embed,view=EmbedView())
        # self.lastmessage: discord.message = await channel.fetch_message(channel.last_message_id)
        # while True:
        #     async for lastmessage in channel.history(limit=1):
        #         self.lastmessage = lastmessage
        #         if self.lastmessage.id != self.message.id:
        #             #await self.message.delete()
        #             await channel.purge(check=is_starter)
        #             self.message = await channel.send(embed=embed,view=EmbedView())
        #         #print(self.message.embeds[0].title)
        #         #print(self.lastmessage.embeds[0].title)
        #         await asyncio.sleep(300)

    # @commands.Cog.listener()
    # async def on_resumed(self):
    #     guild_id: discord.Guild.id = 303245408539246603
    #     channel_id: discord.TextChannel.id = 1018444002883797013 #'941634559274016778' <- look-up-citizen
    #     channel: discord.TextChannel = self.bot.get_guild(guild_id).get_channel(channel_id)

    #     def is_starter(message):
    #         if self.message.author == self.bot.user:
    #             return True
    #         return False
    #     await channel.purge(check=is_starter)
    #     self.lastmessage: discord.message = await channel.fetch_message(channel.last_message_id)
    #     if not 'detailsEmbed' in self.lastmessage.embeds:
    #         self.message = await channel.send(embed=embed,view=EmbedView())


def setup(bot):
    bot.add_cog(viperainteractables(bot))
