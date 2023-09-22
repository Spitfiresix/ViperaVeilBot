import discord
import datetime

_queue = {
    '1v1': [],
    '2v2': [],
    '3v3': [],
    '4v4': []
}

_maxqueue = {
    '1v1': 2,
    '2v2': 4,
    '3v3': 6,
    '4v4': 8
}

def isVerified(ctx: discord.Interaction):
    for role in ctx.guild.roles:
        role: discord.Role = role
        if 'RSI Verified' in role.name:
            role_presence = role.id
    if not role_presence:
        return 'Roles not configured correctly, please create a role called "RSI Verified"'
    verified = False
    for role in ctx.user.roles:
        if role_presence == role.id:
            verified = True
    if not verified:
        return """You are not yet verified, please verify your RSI account by typing /link followed by your RSI Handle.
Example: /link the_Gunner"""
    return 'Success'

async def queue_num(ctx: discord.Interaction, mode: str):
    has_removed = False
    for member in _queue[mode]:
        if ctx.user.id == member[0]:
            _queue[mode].remove(member)
            await ctx.response.send_message(content=f'You have been removed from the {mode} queue!', ephemeral=True, delete_after=30)
            has_removed = True
    if not has_removed:
        _queue[mode].append((ctx.user.id,datetime.datetime.now()))
        await ctx.response.send_message(content=f'You have been added to the {mode} queue!', ephemeral=True, delete_after=30)

async def addQueue(ctx: discord.Interaction, mode: str):
    if mode in _queue:
        await queue_num(ctx, mode)
    else:
        return 'Error, no mode selected. How did you do that?'
    return _queue
    
async def queue_ready(self, ctx: discord.Interaction):
    for mode in _queue:
        if len(mode) >= _maxqueue[mode]:
            print(f'Enough players for {mode} session')

            vipera_guild: discord.Guild = self.bot.get_guild(303245408539246603)
            queue_channel: discord.TextChannel = vipera_guild.get_channel(1074878042712834199)
            
            await queue_channel.send(content=f'Enough members for {mode}, creating lobby now', delete_after=60)
            current_queue_string = ''
            match_players = []
            for players in mode:
                current_queue_string += players + '\n'
                if len(match_players) < _maxqueue[mode]:
                    match_players.append(players)
            
            