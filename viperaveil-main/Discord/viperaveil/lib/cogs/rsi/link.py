import discord
import json
from sqlalchemy.sql import func
from datetime import datetime
from viperaveil.lib.cogs.api import *
from viperaveil.utilities.ApiCalls import CreateViperaUser, GetRSIBio, GetRSIUser, get_rsi_account
from viperaveil.lib.database.database import DatabaseConnection
import logging
logger = logging.getLogger('discord')


async def RSILink(self, ctx: discord.Interaction, scusername: str):
    userRecord = await DatabaseConnection.Partial_Register_select_specific(self, handle=scusername)
    rsi_data = get_rsi_account(scusername)
    try:
        rsi_id = rsi_data['data']['member']['id']
    except:
        rsi_id = None
    is_role = False
    for role in ctx.guild.roles:
        role: discord.Role = role
        if 'RSI Verified' in role.name:
            role_presence = role.id
            verified_role = role
            is_role = True
    if not is_role:
        await ctx.response.send_message(embed=discord.Embed(title='', description='Error! Your guild does not have a role named "RSI Verified"', colour=discord.Colour.red()), ephemeral=True, delete_after=12)
        return
    for role in ctx.user.roles:
        role: discord.Role = role
        if role_presence == role.id:
            await ctx.response.send_message(embed=discord.Embed(title='', description="You're already verified!", colour=discord.Colour.dark_green()), ephemeral=True, delete_after=12)
            return
    if not userRecord:
        userRecord = await DatabaseConnection.Partial_Register_select_specific(self, discordid=str(ctx.user.id))
    # userRecord = getVVUser(discord=ctx.user.name)
    if userRecord:
        #await ctx.channel.send(embed=discord.Embed(title='', description=f"DEBUG {userRecord}", colour=discord.Colour.dark_green()), delete_after=60)
        if userRecord[2]:
            playerData = GetRSIBio(userRecord[2])
        #else:
        #    playerData = GetRSIBio(userRecord.handle)
    else:
        playerData = GetRSIBio(scusername)
    if (playerData == 'Player does not exist') and (scusername):
        await ctx.response.send_message(embed=discord.Embed(title='', description='Error! Username does not exist, please recheck it', colour=discord.Colour.red()), ephemeral=True, delete_after=12)
        return
    if isinstance(playerData, dict):
        if playerData.get('handle'):
            scusernamelocal = playerData['handle']
    if userRecord and not await DatabaseConnection.Partial_Register_select_specific(self=self, handle=scusername) and scusername:
        if not userRecord[2] == scusername:
            key = getKey()
            await DatabaseConnection.Partial_Register_Update(self, rsi_id=rsi_id, discordid=str(ctx.user.id), handle=playerData['handle'], discord=ctx.user.name, key=key)
            await ctx.response.send_message(embed=discord.Embed(title='', description=f'To link your Discord to another RSI account, please enter this key **{key}** into the new accounts Bio, then rerun /link', colour=discord.Colour.orange()), ephemeral=True, delete_after=40)
            return

    if not scusername:
        if not userRecord:
            await ctx.response.send_message(embed=discord.Embed(title='', description='No key found for your RSI Handle, please rerun this command with your RSI handle on the end', colour=discord.Colour.red()), ephemeral=True, delete_after=12)
            return
        else:
            if isinstance(playerData, dict):
                if playerData['bio'].__contains__(userRecord[3]):
                    ###### Post verification!!!! ##################
                    discordData = {
                        'discord_id': str(ctx.user.id),
                        'display_name': ctx.user.display_name,
                        'name': ctx.user.name,
                        'nick': ctx.user.nick,
                        'joined_at': str(ctx.user.joined_at)
                    }
                    User = {
                        'DiscordUserID': str(ctx.user.id),
                        'DiscordHandle': ctx.user.name,
                        'RSIUserID': rsi_id,
                        'RSIHandle': playerData['handle'],
                        'discordData': discordData
                    }
                    # Api Call
                    response = CreateViperaUser(User)
                    await ctx.response.send_message(embed=discord.Embed(title='', description='RSI Account verified!', colour=discord.Colour.dark_green()), ephemeral=True, delete_after=12)
                    await ctx.user.add_roles(verified_role)
                    return 'verified', playerData['org']
                else:
                    await ctx.response.send_message(embed=discord.Embed(title='', description=f'Key not found in your Bio, please add it - {userRecord[3]}', colour=discord.Colour.red()), ephemeral=True, delete_after=40)
                    return
    else:
        if not userRecord:
            key = getKey()
            await DatabaseConnection.Partial_Register_insert(self, rsi_id=rsi_id, discordid=str(ctx.user.id), handle=playerData['handle'], discord=ctx.user.name, key=key)
            await ctx.response.send_message(embed=discord.Embed(title='', description=f'Your key is **{key}**, this needs to go into the Bio on your RSI account - {playerData["handle"]}', colour=discord.Colour.orange()), ephemeral=True, delete_after=40)
            return
        else:
            if playerData['bio'].__contains__(userRecord[3]):
                ###### Post verification!!!! ##################
                discordData = {
                    'discord_id': str(ctx.user.id),
                    'display_name': ctx.user.display_name,
                    'name': ctx.user.name,
                    'nick': ctx.user.nick,
                    'joined_at': str(ctx.user.joined_at)
                }
                User = {
                    'DiscordUserID': str(ctx.user.id),
                    'DiscordHandle': ctx.user.name,
                    'RSIUserID': rsi_id,
                    'RSIHandle': playerData['handle'],
                    'discordData': discordData
                }
                # Api Call
                response = CreateViperaUser(User)
                await ctx.response.send_message(embed=discord.Embed(title='', description='RSI Account verified!', colour=discord.Colour.dark_green()), ephemeral=True, delete_after=12)
                await ctx.user.add_roles(verified_role)
                return 'verified', playerData['org']
            else:
                await ctx.response.send_message(embed=discord.Embed(title='', description=f'Key not found in your Bio, please add it - {userRecord[3]}', colour=discord.Colour.red()), ephemeral=True, delete_after=12)
                return
