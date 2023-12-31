from src.providers.gamemodeprovider import get_game_modes
import discord
from discord.ext import commands

from src.utils.exceptions import get_channel_mode
from src.utils.exceptions import get_game
from src.utils.utils import list_to_int, is_url_image


def is_arg_in_modes():
    def predicate(ctx):
        args = ctx.message.content.split(' ')
        modeslist = get_game_modes()

        if len(args) < 2:
            raise commands.errors.BadArgument(
                "The mode argument is missing.")
        if args[1] not in modeslist:
            raise commands.errors.BadArgument(
                f"The mode is incorrect, you wrote {args[1]}\n"
                f"But it must be in {str(modeslist)}"
                f"But it must be in {str(list(modeslist))}"
            )

        return True

    return commands.check(predicate)


def check_category(*names):
    def predicate(ctx):
        guild = ctx.guild
        ctx_cat = ctx.channel.category
        for name in names:
            to_be_cat = discord.utils.get(guild.categories, name=name)
            if to_be_cat is None:
                raise ValueError(
                    f"The category {name} does not exist or I can't see it.")
            if ctx_cat == to_be_cat:
                return True
        raise commands.errors.BadArgument(
            f"You should write this message in one of {names} category"
        )

    return commands.check(predicate)


# def args_at_pos_digits(lst_pos_args):
#     def predicate(ctx):
#         args = ctx.message.content.split()[1:]
#         return all(args[i].isdigit() for i in lst_pos_args)
#     return commands.check(predicate)


def rank_update(games, lst_pos_args):
    def args_at_pos_digits(args):
        return all(i < len(args) and args[i].isdigit() for i in lst_pos_args)

    def max_greater_min(args):
        from_points, to_points = list_to_int(args[3: 4])
        return from_points < to_points

    def url_image(args):
        return is_url_image(args[2])

    def name_in_rank(ctx, args):
        return args[1] not in games[ctx.guild.id].ranks[int(args[0])]

    def predicate(ctx):
        args = ctx.message.content.split()[1:]

        return args_at_pos_digits(args) and max_greater_min(args)\
            and url_image(args) and name_in_rank(ctx, args)
    return commands.check(predicate)


def has_role_or_above(role_name):
    def predicate(ctx):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None or ctx.author.top_role >= role:
            return True
        raise commands.errors.BadArgument(
            f"You don't have the permission to run this command.\n"
            f"You must be at least {role_name}."
        )
    return commands.check(predicate)


def check_if_banned(games):
    def predicate(ctx):
        game = games[ctx.guild.id]
        id = ctx.author.id
        if id in game.bans:
            game.remove_negative_bans()
            # the ban might have been removed in the function above
            if id in game.bans:
                raise commands.errors.BadArgument(str(game.bans[id]))
        return True
    return commands.check(predicate)


def check_captain_mode(games):
    def predicate(ctx):
        game = games[ctx.guild.id]
        mode = get_channel_mode(ctx)
        if mode not in game.available_modes:
            return False
        queue = game.queues[mode]
        if queue.mode < 2:
            raise commands.errors.BadArgument("This mode does not allow picks")
        if not queue.has_queue_been_full:
            raise commands.errors.BadArgument(
                "The pick session hasn't started")
        return True
    return commands.check(predicate)
