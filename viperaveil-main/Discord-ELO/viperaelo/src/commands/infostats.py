from src.providers.leaderboardproviders import get_leaderboard
from discord import Embed
from discord.ext import commands

from src.utils.decorators import is_arg_in_modes
from src.utils.exceptions import get_game
from src.utils.exceptions import get_player_by_id, get_player_by_mention
from src.utils.utils import add_scroll
from src.utils.utils import get_player_lb_pos, most_stat_embed
from src.utils.utils import team_name
from src.utils.constants import *
from src.providers.gamemodeprovider import get_game_modes
from src.providers.banprovider import get_bans
class InfoStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['lb'])
    @commands.guild_only()
    # @set_default_mode
    @is_arg_in_modes()
    async def leaderboard(self, ctx, mode, stat_key="elo"):
        """Show current leaderboard.

        Example: !lb 1 wins
        Will show the leaderboard of the mode 1vs1 based on the wins.
        [mode] can be any mode in !modes.
        [stats key] can be any stat in !info. e.g:
        name, elo, wins, losses, nb_matches, wlr
        most_wins_in_a_row, most_losses_in_a_row.
        By default, if the stats key is missing, the bot will show the elo lb.
        """
        lb = get_leaderboard(mode)
        
        game = get_game(ctx)
        msg = await ctx.send(embed=game.embed_leaderboard(mode, stat_key, 1, lb))
        await add_scroll(msg)

    @commands.command(aliases=['nb_players'])
    @commands.guild_only()
    async def limit(self, ctx):
        """Show the current limit to amount of users."""
        game = get_game(ctx)
        msg = '\n'.join([f"{mode}: **[{len(users)} / {game.limit_leaderboards}]** players"
                         for mode, users in game.get_leaderboards().items()])
        await ctx.send(embed=Embed(color=0x00FF00,
                                   title="Amount of users",
                                   description=msg
                                   ))

    @commands.command(aliases=['stats'])
    @is_arg_in_modes()
    @commands.guild_only()
    async def info(self, ctx, mode, mention=""):
        """Show the info of a player.

        Example: !info 1 @Anddy
        With no argument, the !info will show the user's stats.
        With a player_name as argument, if the player exists, this will show
        is stats in the seized mode.
        Can be used only in info_chat channel.
        """
        game = get_game(ctx)
        player = await get_player_by_mention(ctx, mode, mention) if mention \
            else await get_player_by_id(ctx, mode, ctx.author.id)

        pos = get_player_lb_pos(game.leaderboard(mode), player)
        await ctx.send(embed=Embed(color=0x00FF00,
                                   title=game.get_rank_name(mode, player.elo, player),
                                   description=str(player))
                       .set_thumbnail(url=game.get_rank_url(mode, player.elo, player))
                       .set_footer(text=f"Position on leaderboard: {pos}"))

    # @commands.command(aliases=['match'])
    # @is_arg_in_modes()
    # @commands.guild_only()
    # async def info_match(self, ctx, mode, id_game):
    #     """Display the infos of a specific match."""
    #     game = get_game(ctx)
    #     if not id_game.isdigit():
    #         raise commands.errors.MissingRequiredArgument(id_game)
    #     id_game = int(id_game)
    #     req_game, game_not_from_archive = game.get_game(mode, id_game)
    #     if req_game is None:
    #         await ctx.send("I couldn't find the game... Maybe it doesn't exist.")
    #         return
    #     if not game_not_from_archive:
    #         queue, winner, elo = req_game
    #         color = 0xFF0000 if winner == 1 else 0x0000FF
    #         winner_str = team_name(winner)
    #         name, emoji = game.maps_archive[mode][id_game] \
    #             if mode in game.maps_archive and id_game in game.maps_archive[mode] \
    #             else ['map', 'no']
    #         await ctx.send(embed=Embed(color=color,
    #                                    description=f"```"
    #                                                f"{'Id':12}: {id_game}\n"
    #                                                f"{'Winner':12}: {winner_str}\n"
    #                                                f"{'Red team':12}: {team_to_player_name(queue.red_team)}\n"
    #                                                f"{'Blue team':12}: {team_to_player_name(queue.blue_team)}\n"
    #                                                f"{'Elo':12}: {elo} points\n"
    #                                                f"{'Map':12}: {emoji} {name}"
    #                                                f"```"
    #                                    ))
    #     else:
    #         queue = req_game
    #         maps = game.maps_archive[mode][id_game] \
    #             if id_game in game.maps_archive[mode] else 'no map'
    #         if isinstance(maps, tuple):
    #             maps = [maps]
    #         str_maps = ', '.join([f'{emoji}{name}' for name, emoji in maps])
    #         await ctx.send(embed=Embed(color=0x00FF00,
    #                                    description=f"```"
    #                                                f"{'Id':10}: {id_game}\n"
    #                                                f"{'Red team':10}: {team_to_player_name(queue.red_team)}\n"
    #                                                f"{'Blue team':10}: {team_to_player_name(queue.blue_team)}\n"
    #                                                f"{'Map':10}: {str_maps}"
    #                                                f"```"
    #                                    ))

    @commands.command(aliases=['h'])
    @is_arg_in_modes()
    @commands.guild_only()
    async def history(self, ctx, mode, mention=""):
        """Show every matches the user played in.

        Example: !h 1 @Anddy
        With no argument, the !info will show the user's stats.
        With a player_name as argument, if the player exists, this will show
        is stats in the seized mode.
        Can be used only in info_chat channel.
        """
        game = get_game(ctx)
        player = await get_player_by_mention(ctx, mode, mention) if mention \
            else await get_player_by_id(ctx, mode, ctx.author.id)

        msg = await ctx.send(embed=game.embed_history(mode, player))
        await add_scroll(msg)

    @commands.command()
    @commands.guild_only()
    async def modes(self, ctx):
        """Print available modes."""
        modes = get_game_modes()
        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=str(list(modes))))
 
    @commands.command(aliases=['bans'])
    @commands.guild_only()
    async def all_bans(self, ctx):
        """Display all bans."""
        bans = get_bans()
        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=bans))

    @commands.command()
    @is_arg_in_modes()
    @commands.guild_only()
    async def most(self, ctx, mode, mention="", order_key="games", with_or_vs="with"):
        """Show who you played the most with.

        Example: !most losses @Anddy with
        Will show the leaderboard of the people with who you lost the most.
        order_key must € [games, draws, wins, losses]
        is the key the table will be ordered by."""
        game = get_game(ctx)

        player = await get_player_by_mention(ctx, mode, mention) if mention \
            else await get_player_by_id(ctx, mode, ctx.author.id)

        if order_key not in ("games", "draws", "wins", "losses"):
            raise commands.errors.BadArgument(order_key)
        if with_or_vs not in ("with", "vs"):
            raise commands.errors.BadArgument(with_or_vs)

        # most_played_with = build_most_played_with(game, mode, name)
        msg = await ctx.send(embed=most_stat_embed(game, mode, player,
                                                   order_key, with_or_vs=with_or_vs))
        await add_scroll(msg)

def setup(bot):
    bot.add_cog(InfoStats(bot))
