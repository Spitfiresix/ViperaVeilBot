import random
import json

from src.providers.gamemodeprovider import get_game_modes

from src.providers.gamemodeprovider import delete_game_mode
from src.providers.gamemodeprovider import add_game_mode
import discord
from discord import Embed
from discord.ext import commands

from main import GAMES
from src.modules.game import Game
from src.utils.decorators import is_arg_in_modes, has_role_or_above
# from utils.exceptions import get_player_by_id, get_player_by_mention
from src.utils.exceptions import get_game
from src.utils.utils import create_mode_discord
from src.utils.utils import is_url_image
from src.utils.utils import split_with_numbers
from src.utils.constants import *

class Init(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def init_snek_wars(self, ctx):
        """Init the bot in the server.

        Initialize the bot to be ready on a guild.
        This command creates every channel needed for the Bot to work.
        Can be used anywhere. Need to have Vipera Pick Up role
        Read https://github.com/AnddyAnddy/discord-elo-bot/wiki/How-to-set-up
        """
        guild = ctx.guild
        if not discord.utils.get(guild.roles, name=ADMIN_ROLE):
            await guild.create_role(name=ADMIN_ROLE,
                                    # permissions=discord.Permissions.all_channel(),
                                    colour=discord.Colour(0xAA0000))
            await ctx.send("Vipera Pick Up role created. Since I don't know the "
                           "layout of your roles, I let you put this new role above "
                           "normal users.")

        # if not discord.utils.get(guild.categories, name='・─ 🐍 Snek Wars ⚔ ─・'):
        if not discord.utils.get(guild.categories, name=SNEKPICKUPS):
            perms_secret_channel = {
                guild.default_role:
                    discord.PermissionOverwrite(read_messages=False),
                guild.me:
                    discord.PermissionOverwrite(read_messages=True),
                discord.utils.get(guild.roles, name=ADMIN_ROLE):
                    discord.PermissionOverwrite(read_messages=True)
            }

            base_cat = await guild.create_category(name=SNEKPICKUPS)
            await guild.create_text_channel(name=INIT_CHANNEL,
                                            category=base_cat,
                                            overwrites=perms_secret_channel)
            await guild.create_text_channel(name=INFO_CHAT, category=base_cat)
            await guild.create_text_channel(name=QUEUE, category=base_cat)
            await guild.create_text_channel(name=SUBMIT, category=base_cat)
            await guild.create_text_channel(name=GAME_ANNOUNCEMENT,
                                            category=base_cat)
            await guild.create_text_channel(name=BANS,
                                            category=base_cat)
            await guild.create_category(name=SOLOELO)
            await ctx.send("Add game modes")
            modes = get_game_modes()
            for mode in modes:
                num, vs_mode = split_with_numbers(mode)
                if len(mode) == 2 and num.isdigit() and int(num) > 0 and vs_mode in ("s", "t"):
                    game_num = int(num)
                    game_type = {"s": "Solo", "t": "Teams elo"}[vs_mode]
                    game_name = f"{game_num}vs{game_num}"
                    guild = ctx.message.guild
                    await create_mode_discord(game_num, game_type, ctx)
                        
                    # player_role = f"{game_name} Player"
                    # player_role_exists = discord.utils.get(guild.roles, name=player_role)
                    # if not player_role_exists:
                    #     new_role = await guild.create_role(name=player_role,
                    #                                 colour=discord.Colour(random.randint(0, 0xFFFFFF)))
                    # await ctx.send(f"{player_role} role created")
                                      
        if ctx.guild.id not in GAMES:
             GAMES[guild.id] = Game(guild.id)

    @commands.command()
    @has_role_or_above(ADMIN_ROLE)
    @is_arg_in_modes()
    @commands.guild_only()
    async def delete_mode(self, ctx, mode):
        delete_game_mode(mode)
        await ctx.send(embed=Embed(color=0x00FF00,
                                   description="The mode has been deleted, please delete the channel."))

    @commands.command()
    @is_arg_in_modes()
    @commands.guild_only()
    async def set_pick_mode(self, ctx, mode, new_mode):
        """Set the pick_mode to the new_mode set

        new mode:
            0: random teams
            1: balanced teams
            2: random cap, picks 1-1 1-1
            3: best cap, picks 1-1 1-1
            4: random cap, picks 1-2 2-1
            5: best cap, picks 1-2 2-1
        """
        game = get_game(ctx)
        new_mode = int(new_mode)
        if split_with_numbers(mode)[1] == 't':
            await ctx.send("Can't set a pick_mode for team vs team")
            return
        if new_mode not in range(6):
            await ctx.send("Wrong new_mode given, read help pick_mode")
            return
        pick_modes = ["random teams", "balanced random", "random cap (1-1)",
                      "best cap (1-1)", "random cap (1-2 2-1)", "best cap (1-2 2-1)"]
        game.queues[mode].mode = new_mode
        if len(game.queues[mode].modes) <= 4:  # backward compatibility
            game.queues[mode].modes.append(game.queues[mode].modes[2])
            game.queues[mode].modes.append(game.queues[mode].modes[3])
        game.queues[mode].pick_function = game.queues[mode].modes[new_mode]
        await ctx.send(f"Pick mode changed to {pick_modes[new_mode]} !")

def setup(bot):
    bot.add_cog(Init(bot))
