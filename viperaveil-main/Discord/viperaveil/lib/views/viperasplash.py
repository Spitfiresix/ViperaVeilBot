import discord
from discord import app_commands, ui, Interaction
from discord.ext import commands
from viperaveil.lib.cogs.rsi.lookup import RSILookup
from viperaveil.lib.cogs.rsi.link import RSILink
from viperaveil.lib.database.database import DatabaseConnection

# class rsiLookupModal(ui.Modal, title = 'RSI Lookup'):
#     scusername = ui.TextInput(label = 'RSI Handle', style = discord.TextStyle.short, placeholder = "RSI Handle To Seach For", required = True)

#     async def on_submit(self, ctx: Interaction):
#         await RSILookup(self, ctx, self.scusername)

# class rsiLinkModal(ui.Modal, title = 'RSI Link'):
#     def __init__(self):
#         self.session = DatabaseConnection.GetSession(self)
#         super().__init__(timeout=None)
#     scusername = ui.TextInput(label = 'RSI Handle', style = discord.TextStyle.short, placeholder = "Your RSI Handle", required = True)

#     async def on_submit(self, ctx: Interaction):
#         await RSILink(self, ctx, self.scusername)

# class viperaEmbedView(discord.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)
#         self.add_item(discord.ui.Button(label='Join the Org!', emoji='<:SNEK:1038010133072052245>', url='https://discord.com/channels/303245408539246603/995852958304583870'))

#     @discord.ui.button(custom_id='EmbedViewRSIButton', label='RSI Lookup', emoji='<:MonkaThink:896698581585653800>', style=discord.ButtonStyle.green)
#     async def rsiButton(self, ctx: discord.Interaction, button: discord.ui.Button):
#         await ctx.response.send_modal(rsiLookupModal())

#     @discord.ui.button(custom_id='EmbedViewRSILink', label='RSI Link', emoji='➕',style=discord.ButtonStyle.blurple)
#     async def rsiLink(self, ctx: discord.Interaction, button: discord.ui.Button):
#         await ctx.response.send_modal(rsiLinkModal())
