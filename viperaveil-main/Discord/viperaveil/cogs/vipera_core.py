"""
Vipera Core cog
"""
import asyncio
import traceback
import sys
import datetime
import logging
import discord
import requests
import json

from discord.ext import tasks, commands
#from moviepy.editor import VideoFileClip
#from pygifsicle import optimize
from viperaveil.utilities.Constants import TT_API_WATCHERS, TT_API, TT_HEADERS
from viperaveil.lib.cogs.vipera.embed import viperaInfoEmbed, gabsInfoEmbed, viperaEventLeaderboard, viperaRanksEmbed, viperaStandardsEmbed, viperaLinksEmbed, viperaSnekWarsEmbed, vipera_ticket
from viperaveil.utilities.database.Server import DBServer
from viperaveil.utilities.database.external_log import DBExtLog
from viperaveil.lib.cogs.tiktok.lookup import tt_lookup

logger = logging.getLogger('discord')

game = discord.Game("with the SNEKs")


class ViperaCore(commands.Cog):
    """ViperaCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @commands.Cog.listener()
    async def on_ready(self):
        """Function runs when the bot reports ready"""
        await asyncio.sleep(2)
        print(f'\n\nLogged in as: {self.bot.user.name} - {self.bot.user.id} \
        Version: {discord.__version__}\n')
        # Changes our bots Playing Status.
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        print('Successfully logged in and booted...!')

        # Check if each server is in the DB
        print("Database check")
        servers = DBServer(self.bot.db_connection).display()
        servers_id = [int(i[0]) for i in servers]
        for guild in self.bot.guilds:
            if guild.id not in servers_id:
                DBServer(
                    self.bot.db_connection).add(
                    guild.id, "?", False, False, False, "", 100)
                print(f"* {guild.name} ({guild.id}) added")

        # Importing loops to run
        ViperaCore.update_vipera_info.start(self)  # pylint: disable=no-member
        ViperaCore.update_gabs_info.start(self)  # pylint: disable=no-member
        ViperaCore.update_event_leaderboard.start(self)  # pylint: disable=no-member
        ViperaCore.update_vipera_information_channel.start(self)  # pylint: disable=no-member
        #ViperaCore.update_snek_wars.start(self)  # pylint: disable=no-member
        ViperaCore.update_vipera_ticket.start(self)  # pylint: disable=no-member
        #ViperaCore.check_tt_upload.start(self)  # pylint: disable=no-member
        
        guildlist = []
        for guild in self.bot.guilds:
            guildlist.append(guild.name)
        print(f"Joined {guildlist}")
        if not discord.opus.is_loaded():
            try:
                discord.opus.load_opus('/usr/lib/libopus.so')
                print('Opus loaded from /usr/lib/libopus.so')
            except BaseException:  # pylint: disable=bare-except,broad-except
                print("Opus loading errored, or you're running this on Windows")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Event pings when bot joins guild"""
        print(f"Joined {guild.name}")
        #print(f'Syncing slash commands for {guild.name}')
        #self.bot.tree.copy_global_to(guild=guild)
        #await self.bot.tree.sync(guild=guild)
        servers = DBServer(self.bot.db_connection).display()
        servers_id = [int(i[0]) for i in servers]
        for guild in self.bot.guilds:
            if guild.id not in servers_id:
                DBServer(
                    self.bot.db_connection).add(
                    guild.id, "?", False, False, False, "", 100)
                print(f"* {guild.name} ({guild.id}) added")

    @tasks.loop(hours=24.0)
    async def update_vipera_info(self):
        """Update Vipera Info embed on loop"""
        vipera_guild: discord.Guild = \
            self.bot.get_guild(303245408539246603)
        vipera_info_channel: discord.TextChannel = \
            vipera_guild.get_channel(995852958304583870)
        vipera_info_message: discord.Message = \
            vipera_info_channel.get_partial_message(1051293750871203851)
        await vipera_info_message.edit(embeds=viperaInfoEmbed())

    @tasks.loop(hours=24.0)
    async def update_vipera_ticket(self):
        """Update Vipera Ticket embed on loop"""
        vipera_guild: discord.Guild = \
            self.bot.get_guild(303245408539246603)
        vipera_info_channel: discord.TextChannel = \
            vipera_guild.get_channel(1020990574796480532)
        vipera_info_message: discord.Message = \
            vipera_info_channel.get_partial_message(1088793776455163944)
        await vipera_info_message.edit(embed=vipera_ticket(self))

    @tasks.loop(hours=24.0)
    async def update_vipera_information_channel(self):
        """Update Vipera Standards embeds on loop"""
        vipera_guild: discord.Guild = \
            self.bot.get_guild(303245408539246603)
        information_channel: discord.TextChannel = \
            vipera_guild.get_channel(995971202097090621)
        information_channel_ranks_message: discord.Message = \
            information_channel.get_partial_message(1067253612952174612)
        await information_channel_ranks_message.edit(embed=viperaRanksEmbed())
        information_channel_ranks_message: discord.Message = \
            information_channel.get_partial_message(1067253614386610206)
        await information_channel_ranks_message.edit(embed=viperaStandardsEmbed())
        information_channel_ranks_message: discord.Message = \
            information_channel.get_partial_message(1067253615674281984)
        await information_channel_ranks_message.edit(embed=viperaLinksEmbed())

    @tasks.loop(hours=24.0)
    async def update_gabs_info(self):
        """Update Gabs Info embed on loop"""
        vipera_guild: discord.Guild = \
            self.bot.get_guild(303245408539246603)
        gabs_info_channel: discord.TextChannel = \
            vipera_guild.get_channel(408434855152451604)
        gabs_info_message: discord.Message = \
            gabs_info_channel.get_partial_message(1050371667144216597)
        await gabs_info_message.edit(embed=gabsInfoEmbed())

    @tasks.loop(hours=24.0)
    async def update_event_leaderboard(self):
        """Update Events Leaderboard embed on loop"""
        vipera_guild: discord.Guild = \
            self.bot.get_guild(303245408539246603)
        event_leaderboard_channel: discord.TextChannel = \
            vipera_guild.get_channel(1048408325152317470)
        event_leaderboard_info_message: discord.Message = \
            event_leaderboard_channel.get_partial_message(1058398182435983431)
        await event_leaderboard_info_message.edit(embed=viperaEventLeaderboard())

    # @tasks.loop(hours=24.0)
    # async def update_snek_wars(self):
    #     """Update SNEK Wars embed on loop"""
    #     vipera_guild: discord.Guild = \
    #         self.bot.get_guild(303245408539246603)
    #     snek_wars_channel: discord.TextChannel = \
    #         vipera_guild.get_channel(1074877620082184284)
    #     snek_wars_message: discord.Message = \
    #         snek_wars_channel.get_partial_message(1076559097517842522)
    #     await snek_wars_message.edit(embed=viperaSnekWarsEmbed())

    @tasks.loop(minutes=5.0)
    async def check_tt_upload(self):
        """Checks for new uploads on watched TT channels"""
        print('Checking for new TikTok videos')
        for username in TT_API_WATCHERS:
            data = tt_lookup(username[0])
            while data is str:
                while data.get('data').get('latest_vid').get('id') == '':
                    try:
                        data = tt_lookup(username[0])
                    except:
                        data = ''
            existing_vid = DBExtLog(self.bot.db_connection).get_by_video_id(video_id=data['data']['latest_vid']['id'])
            if len(existing_vid) > 0:
                pass
            else:
                DBExtLog(self.bot.db_connection).delete(username[0])
                # try:
                #     params = {"link":data['data']['latest_vid']['url']}
                #     resp = requests.request("GET", TT_API, headers=TT_HEADERS, params=params)
                #     resp_json = json.loads(resp.text)
                #     print(resp_json['videoLinks']['download'])
                #     resp = requests.get(resp_json['videoLinks']['download'])
                #     with open(file=f"./viperaveil/cache/{data['data']['latest_vid']['id']}.mp4", mode='wb') as f:
                #         for chunk in resp.iter_content(chunk_size=1024*1024):
                #             if chunk:
                #                 f.write(chunk)
                # except Exception as e:
                #     print('Failed to retrieve download from API')
                #     #print(f'Error: ' + e)
                #     return
                # videoClip = VideoFileClip(f"./viperaveil/cache/{data['data']['latest_vid']['id']}.mp4")
                # cropped = videoClip.subclip(t_start=0, t_end=6)
                # cropped.write_gif(f"./viperaveil/cache/{data['data']['latest_vid']['id']}.gif")
                #optimize(f"./viperaveil/cache/{data['data']['latest_vid']['id']}.gif")
                vipera_guild: discord.Guild = \
                    self.bot.get_guild(303245408539246603) # VV - 303245408539246603, RS - 643051006782996491
                match username[1]:
                    case 'org':
                        content_channel: discord.TextChannel = \
                            vipera_guild.get_channel(998786333378093056) # VV - 998786333378093056, RS - 643072384001114112
                        at_role: discord.Role = vipera_guild.get_role(1096189578689380432)
                    case 'gabs':
                        content_channel: discord.TextChannel = \
                            vipera_guild.get_channel(922582765130629170) # VV - 922582765130629170, RS - 643072384001114112
                        at_role: discord.Role = vipera_guild.get_role(1013206371648413717)
                # embed_gif = f"./viperaveil/cache/{data['data']['latest_vid']['id']}.gif"
                # attach_gif = discord.File(embed_gif)
                # details_embed = discord.Embed(
                #     title=username[0] + ' on TikTok',
                #     url=data["data"]["latest_vid"]["url"],
                #     description=data['data']['latest_vid']['title'],
                #     colour=discord.Colour.dark_green()
                # )
                # details_embed.set_image(url=f"attachment://{data['data']['latest_vid']['id']}.gif")
                # details_embed.set_author(name='TikTok')
                # details_embed.set_footer(icon_url='https://cdn-assets-us.frontify.com/s3/frontify-enterprise-files-us/eyJwYXRoIjoidGlrdG9rXC9hY2NvdW50c1wvMDlcLzQwMDA5NDNcL3Byb2plY3RzXC8zXC9hc3NldHNcL2IyXC82MDFcLzE1OTdmYTJmNGNhM2E2OTNhMTBiNWEzYTBmMGNiNTQ0LTE2MTEzMTY0ODQucG5nIn0:tiktok:HL5FyMM7ye_cjuCVBis02fEokxwX57ulkIqEg0O3XTw?width={width}&rect=0,0,1580,384&reference_width=1580')
                #details_embed.add_field(name='‎', value=at_role.mention)

                #announcement: discord.Message = await content_channel.send(file=attach_gif, embed=details_embed)

                announcement: discord.Message = await content_channel.send(content=f'{at_role.mention} {data["data"]["latest_vid"]["url"]}')
                #await content_channel.send(content=at_role.mention)

                #await announcement.publish()

                DBExtLog(self.bot.db_connection).add('tiktok',username[0],data['data']['latest_vid']['id'], str(vipera_guild.id))
        

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """Event called when user changes occur in guild"""
        for role in after.roles:
            if role not in before.roles:
                # Spot for pushing manual updates to an API
                print(f'{after.name} has been added to role {role.name}')
        for role in before.roles:
            if role not in after.roles:
                # Spot for pushing manual updates to an API
                print(f'{after.name} has been removed from role {role.name}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """On command error send details to Redshift"""
        print(error)
        channel = self.bot.get_channel(643072384001114112)
        if channel is not None:
            try:
                invite = await ctx.guild.channels[0].create_invite()
            except BaseException:  # pylint: disable=bare-except,broad-except
                invite = None
            embed = discord.Embed(
                title="**ERROR :**",
                description="**Date :** " +
                datetime.datetime.now().strftime("%x at %X") +
                f"""**Command name :** {ctx.command.name}
            **Server link :** <{invite}>\n\n```{error}```""",
                color=discord.Colour.red())
            embed.set_footer(
                text=f"""Server : {ctx.guild.name} - {ctx.guild.id}
                 | Author : {ctx.author} - {ctx.author.id}"""
            )
            await channel.send(embed=embed)

            print(
                "\n\n⚠️ ⚠️ ⚠️ " +
                datetime.datetime.now().strftime("%x at %X") +
                f" Ignoring exception in command {ctx.command}\n:",
                file=sys.stderr)
            traceback.print_exception(
                type(error),
                error,
                error.__traceback__,
                file=sys.stderr)
            
    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        """On command error send details to Redshift"""
        print(error)
        channel = self.bot.get_channel(643072384001114112)
        if channel is not None:
            try:
                invite = await ctx.guild.channels[0].create_invite()
            except BaseException:  # pylint: disable=bare-except,broad-except
                invite = None
            embed = discord.Embed(
                title="**ERROR :**",
                description="**Date :** " +
                datetime.datetime.now().strftime("%x at %X") +
                f"""**Command name :** {ctx.command.name}
            **Server link :** <{invite}>\n\n```{error}```""",
                color=discord.Colour.red())
            embed.set_footer(
                text=f"""Server : {ctx.guild.name} - {ctx.guild.id}
                 | Author : {ctx.author} - {ctx.author.id}"""
            )
            await channel.send(embed=embed)

            print(
                "\n\n⚠️ ⚠️ ⚠️ " +
                datetime.datetime.now().strftime("%x at %X") +
                f" Ignoring exception in command {ctx.command}\n:",
                file=sys.stderr)
            traceback.print_exception(
                type(error),
                error,
                error.__traceback__,
                file=sys.stderr)


def setup(bot):
    """Imports Cog class on module import"""
    bot.add_cog(ViperaCore(bot))
