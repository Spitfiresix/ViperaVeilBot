import pickle as _pickle
import asyncio
import os
import sys
from datetime import datetime
import json
import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv, find_dotenv

import src
from src.GAMES import GAMES
from src.modules import game, player, queue_elo, elo, ban
from src.modules.game import Game
from src.utils.exceptions import PassException, send_error
from src.utils.utils import build_other_page
from src.modules.game import DEBUG_UNTIL_BETTER

sys.modules['modules'] = src.modules
sys.modules['modules.game'] = game
sys.modules['modules.player'] = player
sys.modules['modules.queue_elo'] = queue_elo
sys.modules['modules.elo'] = elo
sys.modules['modules.ban'] = ban


PATH = find_dotenv(".env")

#config = dotenv_values(PATH)

load_dotenv()

if not (os.environ.get('DEBUG_MODE') == 'True'):
    TOKEN = os.environ.get('DISCORD_TOKEN')
    API_ENDPOINT = os.environ.get('API_ENDPOINT')
else:
    TOKEN = os.environ.get('DEV_DISCORD_TOKEN')
    API_ENDPOINT = os.environ.get('DEV_API_ENDPOINT')

# TOKEN = os.getenv('DISCORD_TOKEN')
# API_ENDPOINT = os.getenv('API_ENDPOINT')
# test guild
# DISCORD_MAIN_GUILD_ID = 303245408539246603
# real guild
DISCORD_MAIN_GUILD_ID = 303245408539246603
#intents = discord.Intents.default()
#intents.members = True
intents = discord.Intents.all()
BOT: Bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
BOT.load_extension('src.commands.admin')
BOT.load_extension('src.commands.core')
BOT.load_extension('src.commands.helper')
BOT.load_extension('src.commands.infostats')
BOT.load_extension('src.commands.init')
BOT.load_extension('src.commands.matchprocess')
BOT.load_extension('src.commands.graphs')

def assign_game(guild_id, game):
    GAMES[guild_id] = game

@BOT.command(hidden=True)
async def ubotdate(ctx):
    res = '\n'.join([f"{guild.name:20} by {str(guild.owner):20} {len(guild.members)} users"
                     for guild in BOT.guilds if "discord" not in guild.name.lower()])
    total_user = sum([len(guild.members) for guild in BOT.guilds])
    await BOT.change_presence(activity=discord.Game(name=f"{len(BOT.guilds)} guilds with {total_user} users"))
    await ctx.send(
        embed=Embed(color=0x00FF00,
                    title="Guilds infos",
                    description=res)
    )

@BOT.event
async def on_ready():
    """On ready event."""
    print(f'{BOT.user} has connected\n')
    total_user = 0
    for guild in BOT.guilds:
        print(f'{guild.name:20} by + {str(guild.owner):20} {len(guild.members)} users')
        if guild.name.lower() != "top.gg":
            total_user += len(guild.members)
        # load game from service           
        # create new game
        game = Game(guild.id)
        
        assign_game(guild.id, game)

    print(f'\n\n{total_user} users in total, with {len(BOT.guilds)} guilds')
    await BOT.change_presence(activity=discord.Game(name=f"{len(BOT.guilds)} guilds with {total_user} users"))


@BOT.event
async def on_guild_join(guild):
    """Send instruction message on join."""
    print(f"I just joined the guild {guild} {guild.id}")
    channel = next(channel for channel in guild.channels
                   if channel.type == discord.ChannelType.text)
    await channel.send(embed=Embed(color=0x00A000,
                                   title="Hey, let's play together !",
                                   description="Oh hey i'm new around here !\n"
                                               "To set me up, someone will have to "
                                               "write `!init_snek_wars` somewhere and the black magic "
                                               "will handle the rest.\n"
                                               "Any issue ? https://discord.gg/somediscord"))


@BOT.event
async def on_reaction_add(reaction, user):
    """

    @param user: discord.User
    @type reaction: discord.Reaction
    """
    res = build_other_page(BOT, GAMES[user.guild.id], reaction, user)
    if res is None:
        return
    await reaction.message.edit(embed=res)

    await reaction.message.remove_reaction(reaction.emoji, user)


@BOT.event
async def on_command_completion(ctx):
    """Save the data after every command."""

@BOT.event
async def on_command(ctx):
    if DEBUG_UNTIL_BETTER != []:
        await ctx.send(embed = Embed(color=0x000000,
                      description="The server was premium and it is not anymore... This leaderboard can still be reached if the premium is back. You can add this mode with the temporary leaderboard, it will not erase past data."))
        DEBUG_UNTIL_BETTER.clear()
        return


@BOT.event
async def on_command_error(ctx, error):
    inv = ctx.invoked_with
    embed = ""


    if isinstance(error, commands.errors.CommandNotFound):
        embed = Embed(color=0x000000,
                      description="The command doesn't exist, check !cmds !")

    elif isinstance(error, commands.errors.BadArgument):
        await send_error(ctx, error)
        await ctx.message.delete(delay=3)
        return

    elif isinstance(error, commands.errors.CheckFailure):
        embed = Embed(color=0x000000,
                      description="You used this command with either a wrong channel "
                                  + "or a wrong argument. Or you don't have the permission...\n")
        # await ctx.send_help(inv)

    elif isinstance(error, commands.errors.MissingPermissions):
        embed = Embed(color=0x000000,
                      description="You must have manage_roles permission to run that.")

    elif isinstance(error, commands.errors.MissingRequiredArgument):
        embed = Embed(color=0x000000,
                      description=f"{str(error)}\nCheck !help {inv}")
    elif isinstance(error, commands.DisabledCommand):
        embed = Embed(color=0x000000,
                      description="The command is disabled.")

    elif isinstance(error, discord.errors.Forbidden):
        embed = Embed(color=0x000000,
                      description="I don't have permissions to do that.")
        pass
    elif hasattr(error, "original") and isinstance(error.original, PassException):
        pass
    else:
        print(ctx)
        print(ctx.invoked_with, ctx.guild, datetime.now().strftime("%d %h %I h %M"))
        try:
            await discord.utils.get(ctx.guild.channels, name="bugs") \
                .send(f"{ctx.invoked_with}: \n{error}")
            raise error
        except AttributeError:
            await ctx.send(f"{ctx.invoked_with}: \n{error}\n")
            raise error

    try:
        await ctx.author.send(embed=embed)
        await ctx.message.delete(delay=3)

    except Exception:
#        await ctx.send(f"Please {ctx.author.mention}, allow my dms.")
        pass

BOT.run(TOKEN)
