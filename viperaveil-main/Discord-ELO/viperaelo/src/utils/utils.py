import re
from datetime import datetime
import json
import discord
import requests
from discord import Embed
from src.modules.queue_elo import CAPTAINS
from src.utils.exceptions import get_channel_mode
from src.utils.exceptions import get_game, get_player_by_id, PassException
from src.utils.exceptions import send_error, get_picked_player
from src.utils.constants import LOBBY
import random

def rename_attr(obj, old_name, new_name):
    if hasattr(obj, old_name):
        obj.__dict__[new_name] = obj.__dict__.pop(old_name)
        return True
    return False


def split_with_numbers(name):
    return re.findall(r'[A-Za-z]+|[0-9]+', name)


def is_url_image(url):
    """Return True if the url is an existing image."""
    img_formats = ('image/png', 'image/jpeg', 'image/jpg')
    req = requests.head(url)
    return "content-type" in req.headers and req.headers["content-type"] in img_formats


def team_name(id_team):
    """Return the name of the team from its id."""
    return ('Nobody', 'Red', 'Blue')[id_team]


def list_to_int(list_str):
    """Return the list but every elem is converted to int."""
    return [int(elem) for elem in list_str]


def get_elem_from_embed(reaction):
    mb = reaction.message.embeds[0]
    footer = mb.footer.text.split()

    return {
        "current_page": int(footer[1]),
        "last_page": int(footer[3]),
        "function": mb.fields[0].value,
        "key": mb.fields[1].value,
        "mode": mb.fields[2].value,
        "id": int(mb.fields[3].value) if len(mb.fields) == 4 else None
    }


def get_start_page(reaction, embed):
    allowed_emojis = {"⏮️": 1, "⬅️": embed["current_page"] - 1,
                      "➡️": embed["current_page"] + 1, "⏭️": embed["last_page"]}
    return allowed_emojis[reaction.emoji]


def add_attribute(game, attr_name, value):
    """Add an attribute to every player when I manually update."""
    for mode in game.get_leaderboards():
        for player in game.leaderboard(mode):
            if not hasattr(game.leaderboard(mode)[player], attr_name):
                setattr(game.leaderboard(mode)[player], attr_name, value)


def reset_attribute(game, attr_name, value):
    """Add an attribute to every player when I manually update."""
    for mode in game.get_leaderboards():
        for player in game.leaderboard(mode):
            setattr(game.leaderboard(mode)[player], attr_name, value)


def build_other_page(bot, game, reaction, user):
    reaction.emoji = str(reaction)
    if user.id == bot.user.id or not reaction.message.embeds \
            or reaction.emoji not in "⏮️⬅️➡️⏭️":
        return
    embed = get_elem_from_embed(reaction)

    if embed["function"] not in ["leaderboard", "archived", "undecided",
                                 "canceled", "commands", "ranks", "history", "most", "maps"]:
        return None

    start_page = get_start_page(reaction, embed)
    if embed["function"] == "leaderboard":
        return game.embed_leaderboard(embed["mode"], embed["key"],
                                      start_page)
    elif embed["function"] in ["archived", "undecided", "canceled"]:
        return getattr(game, embed["function"])(embed["mode"],
                                                start_page=start_page)
    elif embed["function"] == "history":
        player = game.leaderboard(embed["mode"])[embed["id"]]
        return getattr(game, embed["function"])(embed["mode"],
                                                player, start_page=start_page)

    elif embed["function"] == "commands":
        return cmds_embed(bot, start_page)

    elif embed["function"] == "maps":
        return getattr(game, embed["function"])(start_page)

    elif embed["function"] == "most":
        order_key, with_or_vs = embed["key"].split()
        return most_stat_embed(game, embed["mode"], embed["id"], order_key, start_page, with_or_vs)
    elif embed["function"] == "ranks":
        return game.display_ranks(embed["mode"], start_page)

    return None


def check_if_premium(before, after):
    if len(before.roles) < len(after.roles):
        new_role = next(
            role for role in after.roles if role not in before.roles)
        role_name = new_role.name.lower().split()
        return "double" in role_name
    return False


def cmds_embed(bot, start_page=1):
    nb_pages = 1 + len(bot.commands) // 15
    nl = '\n'
    return Embed(color=0x00FF00, description='```\n'
                                             + '\n'.join([f'{command.name:15}: {command.help.split(nl)[0]}'
                                                          for command in sorted(bot.commands, key=lambda c: c.name)[
                                                                         15 * (start_page - 1): 15 * start_page]
                                                          if command.help is not None and not command.hidden]) + '```') \
        .add_field(name="name", value="commands") \
        .add_field(name="-", value="-") \
        .add_field(name="-", value=0) \
        .set_footer(text=f"[ {start_page} / {nb_pages} ]")


def most_stat_embed(game, mode, player, order_key="game", start_page=1, with_or_vs="with"):
    player = game.leaderboard(mode)[player] if str(player).isdigit() else player
    most_played_with = build_most_played_with(game, mode, player, with_or_vs)
    len_page = 20
    nb_pages = 1 + len(most_played_with) // len_page
    current_page = len_page * (start_page - 1)
    next_page = len_page * start_page
    order = ["games", "draws", "wins", "losses"].index(order_key)
    return Embed(title=f"Leaderboard of the most played games {with_or_vs} players",
                 color=0x00FF00,
                 description=f'```\n{"name":20} {"game":7} {"draw":7} {"wins":7} {"losses":7}\n'
                             + '\n'.join([
                     f"{name:20} {_with:<7} {d:<7} {w:<7} {l:<7}"
                     for name, (_with, d, w, l) in sorted(most_played_with.items(),
                                                          key=lambda x: x[1][order], reverse=True)[current_page: next_page]]) +
                             "```"
                 ).add_field(name="name", value="most") \
        .add_field(name="key", value=f"{order_key} {with_or_vs}") \
        .add_field(name="mode", value=mode) \
        .add_field(name="id", value=player.id_user) \
        .set_footer(text=f"[ {start_page} / {nb_pages} ]")


def get_player_lb_pos(leaderboard, player):
    """Return the player position in the leaderboard based on the key O(n)."""
    res = 1
    for _, p in leaderboard.items():
        res += getattr(p, "elo") > getattr(player, "elo")
    return res


def build_most_played_with(game, mode, player, with_or_vs):
    most_played_with = {}
    archive = game.archive[mode]
    # player = game.leaderboard(mode)[name]
    for (queue, win, _) in archive.values():
        if player in queue:
            if with_or_vs == "with":
                team = queue.red_team if player in queue.red_team else queue.blue_team
            else:
                team = queue.red_team if player not in queue.red_team else queue.blue_team
            for p in team:
                team_players_stats(p, player, most_played_with, win, queue)
    most_played_with.pop(player.name, None)
    return most_played_with


def team_players_stats(team_player, me, most_played_with, win, queue):
    if team_player.name in most_played_with:
        most_played_with[team_player.name][0] += 1
    else:
        # nb matches with, nb draws, nb wins, nb losses
        most_played_with[team_player.name] = [1, 0, 0, 0]
    if win == 0:
        most_played_with[team_player.name][1] += 1
    elif queue.player_in_winners(win, me):
        most_played_with[team_player.name][2] += 1
    else:
        most_played_with[team_player.name][3] += 1


async def auto_submit_reactions(reaction, user, game, removed=False):
    title = reaction.message.embeds[0].title.split()
    if title[0] != "auto_submit":
        return
    function, mode, id = title
    id = int(id)
    if id not in game.undecided_games[mode]:
        return
    queue = game.undecided_games[mode][id]
    if removed:
        queue.remove_reacted(user.id)
        return
    role = discord.utils.get(reaction.message.guild.roles, name="Vipera Pick Up")
    is_admin = role is None or user.top_role >= role

    if user.id not in game.leaderboard(mode) or \
            game.leaderboard(mode)[user.id] not in queue:
        if not is_admin:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

    reactions = reaction.message.reactions
    maxi, index = 1, 0
    if is_admin:
        maxi, index = 127, ["🟢", "🔴", "🔵", "❌"].index(reaction.emoji)

    else:
        for i, elem in enumerate(reactions):
            if elem.count > maxi:
                maxi, index = elem.count, i
    if maxi - 1 >= queue.max_queue // 2 + 1:
        if index <= 2:  # a team won or a draw
            text, worked = game.add_archive(mode, id, index)
            await reaction.message.channel.send(
                embed=Embed(color=0xFF0000 if index == 1 else 0x0000FF,
                            description=text))
        else:  # game was canceled
            game.cancel(mode, id)
            await reaction.message.channel.send(
                embed=Embed(color=0x00FF00,
                            description=f"The game {id} was canceled"))
        await reaction.message.add_reaction("✅")

    queue.add_reacted(user.id)


async def join_team_reaction(reaction, user, game):
    embed = reaction.message.embeds[0]
    title = embed.title
    if not title:
        return
    title = title.split()
    if title[0] != "Invitations":
        return
    if len(reaction.message.reactions) > 2:
        return

    mode = title[2]
    queue = game.queues[mode]
    players = [game.leaderboard(mode)[int(embed.fields[0].value[2: -1])]]
    for mention in embed.fields[1:]:
        players.append(game.leaderboard(mode)[int(mention.value[3: -1])])
    if user.id not in [p.id_user for p in players]:
        await reaction.message.remove_reaction(reaction.emoji, user)
        return

    if reaction.message.reactions[0].count == len(players):
        await reaction.message.add_reaction("✅")
        embed.title += f" (accepted)"
        await reaction.message.edit(embed=embed)

        ctx = reaction.message.channel
        res = await queue.add_players(ctx, players, game, mode)
        if res:
            await ctx.send(embed=Embed(color=0x00FF00, description=res))
            if queue.is_finished():
                await ctx.send(embed=Embed(color=0x00FF00,
                                           description=game.add_game_to_be_played(queue, mode)))
                await set_map(ctx, game, queue, mode)
                await announce_game(ctx, res, queue, mode)

    elif reaction.message.reactions[1].count > 1:
        await reaction.message.add_reaction("❌")
        embed.title += f" (refused by {user.display_name})"
        await reaction.message.edit(embed=embed)


async def map_pick_reactions(reaction, user, game):
    if reaction.message.embeds[0].title in "Only one map" or \
            "auto_submit" in reaction.message.embeds[0].title:
        return
    embed = get_elem_from_embed(reaction)
    if embed["function"] != "lobby_maps":
        return
    mode, id = embed["mode"], embed["id"]
    if id in game.maps_archive[mode] and isinstance(game.maps_archive[mode][id], tuple):
        return
    queue = game.undecided_games[mode][id]
    if user.id not in game.leaderboard(mode) or \
            game.leaderboard(mode)[user.id] not in queue:
        await reaction.message.remove_reaction(reaction.emoji, user)
        return
    for i, r in enumerate(reaction.message.reactions):
        if r.count - 1 >= queue.max_queue // 2 + 1:
            emoji, name = reaction.message.embeds[0].description.split('\n')[
                i + 1].split()
            game.add_map_to_archive(mode, id, name, emoji)
            await reaction.message.channel.send(embed=Embed(color=0x00FF00,
                                                            description="Okay ! We got enough votes, the map is...\n"
                                                                        f"{emoji} {name}"
                                                            )
                                                )
            return


async def add_emojis(msg, game, mode, id):
    for _, emoji in game.maps_archive[mode][id]:
        await msg.add_reaction(emoji)


async def add_scroll(message):
    """Add ⏮️ ⬅️ ➡️ ⏭️ emojis to the message."""
    for e in ['⏮️', '⬅️', '➡️', '⏭️']:
        await message.add_reaction(e)


async def set_map(ctx, game, queue, mode):
    if queue.map_mode != 0:
        msg = await ctx.send(queue.ping_everyone(),
                             embed=game.embed_lobby_maps(mode, queue.game_id))
        if queue.map_mode == 2:
            await add_emojis(msg, game, mode, queue.game_id)


async def announce_game(ctx, res, queue, mode):
    if res != "Queue is full...":
        emojis = ["🟢", "🔴", "🔵", "❌"]
        channel = discord.utils.get(ctx.guild.channels,
                                    name=LOBBY)
        msg = await channel.send(queue.ping_everyone(),
                                 embed=Embed(color=0x00FF00,
                                             title=f"auto_submit {mode} {queue.game_id}",
                                             description=announce_format_game(queue)))
        for elem in emojis:
            await msg.add_reaction(elem)


async def finish_the_pick(ctx, game, queue, mode, team_just_picked):
    other_team_id = 1 if team_just_picked == 2 else 2
    other_cap = queue.get_team_by_id(other_team_id)[0]
    nb_to_pick = nb_players_to_pick(queue, other_team_id)
    if queue in CAPTAINS:
        CAPTAINS[queue][team_just_picked].stop()
    if len(queue.players) == 1:
        await queue.set_player_team(ctx, other_team_id, queue.players[0])

    else:
        if queue in CAPTAINS:
            await CAPTAINS[queue][other_team_id].start(ctx, game, mode, queue.game_id, other_cap)

        await ctx.send(content=f"<@{other_cap.id_user}> have to pick **{nb_to_pick}** players.\n"
                       f"Time left: **{CAPTAINS[queue][other_team_id].time_left}** s",
                       embed=Embed(color=0x00FF00, description=str(queue)))

    if queue.is_finished():
        CAPTAINS.pop(queue, None)
        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=str(queue)))

        await announce_game(ctx, "", game.queues[mode], mode)
        game.add_game_to_be_played(game.queues[mode], mode)
        if queue.map_mode != 0:
            msg = await ctx.send(queue.ping_everyone(),
                                 embed=game.embed_lobby_maps(mode, queue.game_id))
            if queue.map_mode == 2:
                await add_emojis(msg, game, mode, queue.game_id)


def nb_players_to_pick(queue, my_team_id):
    if queue.mode in (2, 3):
        return 1
    my_team = queue.get_team_by_id(my_team_id)
    other_team = queue.get_team_by_id(1 if my_team_id == 2 else 2)
    if len(queue.players) >= 3:
        return 1 if len(my_team) >= len(other_team) else 2
    return 1


async def pick_players(ctx, queue, mode, team_id, p1, p2):
    nb_p = nb_players_to_pick(queue, team_id)
    if nb_p == 2 and not p2 or nb_p == 1 and p2:
        await send_error(ctx, f"You need to pick **{nb_p}** players.")
        raise PassException()

    lst = [await get_picked_player(ctx, mode, queue, p1)]
    if nb_p > 1:
        lst.append(await get_picked_player(ctx, mode, queue, p2))
        if lst[0] == lst[1]:
            await send_error(ctx, f"You picked twice <@{lst[0].id_user}>.")
            raise PassException()
    for i in range(nb_p):
        await queue.set_player_team(ctx, team_id, lst[i])


async def get_announce_with_id(channel, mode, id):
    messages = await channel.embed_history().flatten()
    for message in messages:
        if message.embeds and message.embeds[0].title \
                and "auto_submit" in message.embeds[0].title:

            m_mode, m_id = message.embeds[0].title.split()[1:]
            if mode == m_mode and int(m_id) == id:
                return message
    return None


async def check_if_submitted(ctx, game, mode, player):
    queue = game.get_last_undecided_game_by(player, mode)
    if queue is None or not hasattr(queue, "reacted") \
            or not queue.reacted or player.id_user in queue.reacted:
        return True

    await send_error(ctx, f"You must react to the game n°{queue.game_id} before joining a new queue.")
    raise PassException()


async def join_aux(ctx, player=None):
    game = get_game(ctx)
    mode = get_channel_mode(ctx)
    
    queue = game.queues.get(mode, {} )
    
    if player is None:
        player = await get_player_by_id(ctx, mode, ctx.author.id)
        await check_if_submitted(ctx, game, mode, player)

    setattr(player, "last_join", datetime.now())
    is_queue_now_full = queue.has_queue_been_full
    res = await queue.add_player(ctx, player, game)
    is_queue_now_full = queue.has_queue_been_full != is_queue_now_full

    await ctx.send(content=queue.ping_everyone() if is_queue_now_full else "",
                   embed=Embed(color=0x00FF00, description=res))

    if queue.is_finished():
        await ctx.send(embed=Embed(color=0x00FF00,
                                   description=game.add_game_to_be_played(queue, mode)))
        await set_map(ctx, game, queue, mode)
        await announce_game(ctx, res, queue, mode)


async def create_mode_discord(nb_p, catName, ctx):
    guild = ctx.message.guild
    cat = discord.utils.get(guild.categories, name=catName)
    await guild.create_text_channel(f'{nb_p}vs{nb_p}', category=cat)
    #await ctx.send(embed=Embed(color=0x00FF00,
    #                           description="The game mode has been added."))
