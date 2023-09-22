from src.modules.player import convert_player_to_dto
from src.dtos.playerdtos import PlayerDtoEncoder
from src.providers.playerprovider import get_player, add_player
from src.providers.leaderboardproviders import add_player_to_leaderboard
from src.providers.gamemodeprovider import get_game_modes
from src.providers.matchmakerprovider import enqueue_player
import discord
import random
from discord import Embed
from discord.ext import commands

from main import GAMES
from src.modules.player import Player
from src.utils.decorators import check_category, is_arg_in_modes, check_if_banned, check_captain_mode
from src.utils.exceptions import PassException
from src.utils.exceptions import get_captain_team
from src.utils.exceptions import get_channel_mode
from src.utils.exceptions import get_game
from src.utils.exceptions import get_player_by_id, get_player_by_mention
from src.utils.exceptions import send_error
from src.utils.utils import finish_the_pick, pick_players, join_aux
from src.utils.utils import join_team_reaction
from src.utils.utils import split_with_numbers
from src.utils.constants import *
import json

class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_reaction_add(self, reaction, user):
        """

        @param user: discord.User
        @type reaction: discord.Reaction
        """
        reaction.emoji = str(reaction)
        if user.id == self.bot.user.id or not reaction.message.embeds:
            return
        game = GAMES[user.guild.id]
        if reaction.emoji in "👍👎":
            await join_team_reaction(reaction, user, game)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_reaction_remove(self, reaction, user):
        if user.id == self.bot.user.id or not reaction.message.embeds:
            return
        game = GAMES[user.guild.id]
        if reaction.emoji in "👍👎":
            await join_team_reaction(reaction, user, game)

    # @commands.command(aliases=['r', 'reg'])
    # @is_arg_in_modes()
    # @commands.guild_only()
    async def register(self, ctx, mode):
        """Register the player to the elo embed_leaderboard.

        Example: !r N or !r N all
        This command will register the user into the game mode set in argument.
        The game mode needs to be the N in NvsN, and it needs to already exist.
        This command can be used only in the register channel.
        The command will fail if the mode doesn't exist (use !modes to check)."""

        name = ctx.author.id
        #add new player
        #add player to leader board
        player = get_player(name)
        if player != None:
            await ctx.send(embed=Embed(color=0x000000,
                                       description=f"There's already a played called <@{name}>."))
            return
        else :
            player = Player(ctx.author.name, ctx.author.id)
            dto  = convert_player_to_dto(player)
            response = add_player(json.dumps(dto, cls=PlayerDtoEncoder))
            add_player_to_leaderboard(player.name, player.elo, mode)
            await ctx.send(embed=Embed(color=0x00FF00,
                                       description=f"<@{name}> has been registered."))
            num = split_with_numbers(mode)[0]
            role = discord.utils.get(
                ctx.guild.roles, name=f"{num}vs{num} Player")
            await ctx.author.add_roles(role)
        
    # @commands.command(aliases=['r_all', 'reg_all'])
    # @commands.guild_only()
    async def register_all(self, ctx):
        """Register to every available modes in one command."""
        modeslist = get_game_modes()
        player = get_player(ctx.author.id)
        if player == None:
             player = Player(ctx.author.name, ctx.author.id)
        player.SelectedModes = modeslist
        playerdto  = convert_player_to_dto(player)
        response = add_player(json.dumps(playerdto, cls=PlayerDtoEncoder))
        for mode in modeslist:
            add_player_to_leaderboard(player.name, player.elo, mode)
            num = int(split_with_numbers(mode)[0])
            role = discord.utils.get(ctx.guild.roles, name=f"{num}vs{num} Elo Player")
            # role may have been deleted...
            if role is not None:
                await ctx.author.add_roles(role)
            else:
                await ctx.message.guild.create_role(name=f"{num}vs{num} Elo Player",
                                                    colour=discord.Colour(random.randint(0, 0xFFFFFF)))
                await ctx.author.add_roles(role)

        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=f"<@{ctx.author.name}> has been registered for every mode."))

    @commands.command(aliases=['quit'], enabled=False)
    @commands.guild_only()
    async def quit_elo(self, ctx):
        """Delete the user from the registered players.

        The user will lose all of his data after the command.
        Can be used only in Bye channel.
        Can't be undone."""
        game = get_game(ctx)
        id = ctx.author.id

        #remove player from database
        #remove players entry from leader boards

        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=f'<@{id}> has been removed from the rankings'))

    @commands.command(pass_context=True, aliases=['j'])
    @check_category(SOLOELO)
    #@check_if_banned(GAMES)
    @commands.guild_only()
    async def join(self, ctx, modes):
        """Let the player join a queue.

        When using it on a channel in Modes category, the user will join the
        current queue, meaning that he'll be in the list to play the next match.
        Can't be used outside Modes category.
        The user can leave afterward by using !l.
        The user needs to have previously registered in this mode."""
        id = ctx.author.id
        player = get_player(id)
        add_player(name, player.elo, modes)
        enqueue_player(player, modes)

    @commands.command(pass_context=True, aliases=['l'])
    @check_category(SOLOELO)
    @commands.guild_only()
    async def leave(self, ctx):
        """Remove the player from the queue.

        As opposite to the !join, the leave will remove the player from the
        queue if he was in.
        Can't be used outside Modes category.
        The user needs to be in the queue for using this command.
        The user can't leave a queue after it went full."""
        game = get_game(ctx)
        mode = get_channel_mode(ctx)
        player = await get_player_by_id(ctx, mode, ctx.author.id)
        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=game.queues[mode].remove_player(player)))

    @commands.command(aliases=['p'])
    @check_category(SOLOELO)
    @check_captain_mode(GAMES)
    @commands.guild_only()
    async def pick(self, ctx, p1, p2=""):
        """Pick a player in the remaining player.

        Let's say Gabs is the red captain, and it's his turn to pick.
        Remaining players:
        1) @orp
        2) @grünersamt
        To pick orp, gabs can either do:
        !p @orp
        or
        !p 1
        """
        game = get_game(ctx)
        mode = get_channel_mode(ctx)
        queue = game.queues[mode]
        team_id = await get_captain_team(ctx, queue, mode, ctx.author.id)
        await pick_players(ctx, queue, mode, team_id, p1, p2)
        await finish_the_pick(ctx, game, queue, mode, team_id)

def setup(bot):
    bot.add_cog(Core(bot))
