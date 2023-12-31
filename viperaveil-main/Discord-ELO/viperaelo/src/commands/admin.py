"""Module used to represent every commands an admin is able to do."""

from src.providers.banprovider import add_ban, unban_user, get_bans
import discord
from discord import Embed
from discord.ext import commands

from src.modules.player import Player
from src.modules.queue_elo import TIMEOUTS
from src.utils.decorators import check_category, is_arg_in_modes, has_role_or_above
from src.utils.exceptions import PassException
from src.utils.exceptions import get_channel_mode
from src.utils.exceptions import get_game
from src.utils.exceptions import get_id
from src.utils.exceptions import get_player_by_mention, send_error
from src.utils.exceptions import get_total_sec
from src.utils.utils import join_aux
from src.utils.utils import split_with_numbers
from src.utils.constants import *

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(aliases=['fr'])
    # @check_category(SOLOELO)
    # @has_role_or_above(ADMIN_ROLE)
    # @commands.guild_only()
    # async def force_remove(self, ctx, mention):
    #     # """Remove the player from the current queue."""
    #     mode = get_channel_mode(ctx)
    #     id = await get_id(ctx, mention)
    #     player = await get_player_by_mention(ctx, mode, mention)
    #     evict_player_from_queue(id)
    #     await ctx.send(embed=Embed(color=0x00FF00,
    #                                 description= f"removed player from queue {player}"))

    @commands.command()
    @has_role_or_above(ADMIN_ROLE)
    @check_category(SNEKWARS)
    @commands.guild_only()
    async def force_quit(self, ctx, mention):
        # """Delete the seized user from the registered players.

  
        # The command is the same than quit_elo except that the user has to make
        # someone else quit the Elo.
        # Can't be undone."""
        # game = get_game(ctx)
        # id = await get_id(ctx, mention)
        # game.erase_player_from_queues(id)
        # game.erase_player_from_leaderboards(id)

         await ctx.send(embed=Embed(color=0x00FF00,
                                    description=f'{mention} has been removed from the rankings'))

   
    @commands.command()
    @has_role_or_above(ADMIN_ROLE)
    @commands.guild_only()
    async def ban(self, ctx, mention, timeUnity, *reason):
        # """Bans the player for a certain time.

        # Example:
        # unity must be in s, m, h, d (secs, mins, hours, days).

        # """
        id = await get_id(ctx, mention)
        time = split_with_numbers(timeUnity)
        unity = ""
        if len(time) == 2:
            time, unity = time
        total_sec = await get_total_sec(ctx, time, unity)
        add_ban(id, total_sec, ' '.join(reason))
        await ctx.send(embed=Embed(color=0x00FF00,
                                    description=f"{mention} has been banned ! Check !bans"))

    @commands.command()
    @has_role_or_above(ADMIN_ROLE)
    @commands.guild_only()
    async def unban(self, ctx, mention):
        """Unban the player."""
        id = await get_id(ctx, mention)
        #Call UnbanPlayer Api
        unban_user(id)
        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=f"{mention} has been unbanned ! Check !bans"))

    @commands.command()
    @is_arg_in_modes()
    @commands.guild_only()
    async def set_elo(self, ctx, mode, name, elo):
        """Set the elo to the player in the specific mode."""
        get_game(ctx).set_elo(mode, int(name[3: -1]), int(elo))
        await ctx.send("Worked!")

    @commands.command()
    @is_arg_in_modes()
    @commands.guild_only()
    async def set_stat(self, ctx, mode, mention, stat_name, value):
        player = await get_player_by_mention(ctx, mode, mention)
        if not value.isdigit():
            await send_error(ctx, "Value must be an integer")
            raise PassException()
        if stat_name in Player.STATS[1: -2]:
            old = getattr(player, stat_name)
            setattr(player, stat_name, int(value))
            await ctx.send(embed=Embed(color=0x00FF00,
                                       description=f"The stat {stat_name} was changed from {old} to {value}"))
        else:
            await send_error(ctx, "You can not modify this stat.")

    @commands.command()
    @is_arg_in_modes()
    @commands.guild_only()
    async def set_all_stats(self, ctx, mode, name, *stats):
        """Set the stats to the player in the specific mode.
        Let any stat to -1 to not let it change.
        In order:
            [elo, wins, losses, nb_matches, wlr, most_wins_in_a_row,
            most_losses_in_a_row, current_win_streak,
            current_lose_streak]
            The wlr will anyway be calculated at the end.
        """
        player = get_game(ctx).leaderboard(mode)[int(name[3: -1])]
        stats_name = Player.STATS[1: -2]
        if len(stats) > len(stats_name):
            await ctx.send("Too much arguments ! I'll cancel in case you messed up")
            return

        for i, stat in enumerate(stats):
            try:
                stat = int(stat)
                if stat >= 0:
                    setattr(player, stats_name[i], stat)
            except ValueError:
                await ctx.send(f"Wrong format for {stats_name[i]}.")

        player.wlr = player.wins / player.losses if player.losses != 0 else 0
        await ctx.send("Worked!")

    @commands.command(aliases=['rmsp'])
    @commands.guild_only()
    async def remove_non_server_players(self, ctx):
        """Remove people that aren't in the server anymore."""
        game = get_game(ctx)
        guild = self.bot.get_guild(ctx.guild.id)
        start = sum(len(v) for mode, v in game.get_leaderboards().items())
        for mode in game.available_modes:
            game.leaderboard[mode] = {
                id: player for id, player in game.leaderboard(mode).items()
                if guild.get_member(id) is not None
            }
        end = sum(len(v) for mode, v in game.get_leaderboards().items())

        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=f"You kicked {start - end} members from the leaderboards"))

def setup(bot):
    bot.add_cog(Admin(bot))
