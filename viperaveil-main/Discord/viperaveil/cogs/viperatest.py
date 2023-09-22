import discord
from discord.ext import commands
from discord import ui, Interaction
import logging
logger = logging.getLogger('discord')


class viperatest(commands.Cog):
    """ViperaTestCog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name='tableflip',
                          description='Name is fairly self explanatory')
    async def tableflip(self, ctx: Interaction):
        """Name is fairly self explanatory"""
        await ctx.channel.send(content='(╯°□°)╯︵ ┻━┻')
        await ctx.response.send_message(content='Table Flipped', ephemeral=True, delete_after=12)

    @discord.slash_command(name='plink',
                           description='Plinks')
    async def plink(self, ctx: Interaction):
        """Jus do eeeiit"""
        await ctx.channel.send(content='https://media.tenor.com/uFb8sQFRNvQAAAAC/plink-cat.gif')
        await ctx.response.send_message(content='Plinked', ephemeral=True, delete_after=12)

    @commands.command(name='roles', hidden=False)
    async def viperatest_roles(self, ctx):
        """Command which displays roles
        for the author of the message"""

        try:
            print(f'Running command "roles for user {ctx.author.name}"')
            roleslist = ''
            for role in ctx.author.roles:
                if not role.name == '@everyone':
                    roleslist = roleslist + role.name + '\n'
            await ctx.channel.send(roleslist)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @discord.slash_command(name='rolenum',
                          description='Number of users in @role')
    async def viperatest_rolenum(self, ctx: discord.Interaction, role: discord.Option(discord.Role, '@Discord Role')):
        """Command which displays the number
        of people in a given role"""
        if 1000868850960715931 in [discRole.id for discRole in ctx.user.roles]:
            try:
                async with ctx.channel.typing():
                    print(
                        f'Running command "rolenum for user {ctx.user.name}"')
                    await ctx.response.send_message(content=f'{len(role.members)} users in {role.mention}')
            except Exception as e:
                await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}', delete_after=12)
        else:
            await ctx.response.send_message(content="You don't have access to run this command", ephemeral=True, delete_after=12)

    @discord.slash_command(name='rolelist', description='List users in @role')
    async def viperatest_rolenum(self, ctx: discord.Interaction, role: discord.Option(discord.Role, '@Discord Role')):
        """Command which displays the number
        of people in a given role"""
        if 1000868850960715931 in [discRole.id for discRole in ctx.user.roles]:
            try:
                async with ctx.channel.typing():
                    print(
                        f'Running command "rolelist for user {ctx.user.name}"')
                    memberString = ''
                    for members in role.members:
                        memberString += f'{members.name}#{members.discriminator} - {members.mention} \n'
                    await ctx.response.send_message(embed=discord.Embed(title=f'{role.name}', description=memberString, colour=role.colour))
            except Exception as e:
                await ctx.channel.send(f'**`ERROR:`** {type(e).__name__} - {e}', delete_after=12)
        else:
            await ctx.response.send_message(content="You don't have access to run this command", ephemeral=True, delete_after=12)


def setup(bot):
    bot.add_cog(viperatest(bot))
