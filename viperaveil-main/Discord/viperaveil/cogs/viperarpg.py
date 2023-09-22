import discord
from discord import ui, Interaction
from discord.ext import commands
from datetime import datetime
import logging
logger = logging.getLogger('discord')


class my_modal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title = 'Example Modal'

        self.add_item(ui.InputText(
        label='Is this working?',
        style=discord.TextStyle.short,
        placeholder="Yes?",
        default="Yes/No",
        required=True))
        self.add_item(ui.InputText(
        label='Is this working?',
        style=discord.TextStyle.short,
        placeholder="Yes?",
        default="Yes/No",
        required=True))
        self.add_item(ui.InputText(
        label='Is this working?',
        style=discord.TextStyle.short,
        placeholder="Yes?",
        default="Yes/No",
        required=True))
        self.add_item(ui.InputText(
        label='Is this working?',
        style=discord.TextStyle.short,
        placeholder="Yes?",
        default="Yes/No",
        required=True))
        self.add_item(ui.InputText(
        label='Is this working?',
        style=discord.TextStyle.short,
        placeholder="Yes?",
        default="Yes/No",
        required=True))

    async def callback(self, interactions: Interaction):
        embed = discord.Embed(
            title=self.title,
            description=f"**{self.children[0].label}**\n{self.children[0]}\n \n \n**{self.children[1].label}**\n{self.children[1]}\n \n \n**{self.children[2].label}**\n{self.children[2]}\n \n \n**{self.children[3].label}**\n{self.children[3]}\n \n \n**{self.children[4].label}**\n{self.children[4]}",
            timestamp=datetime.now(),
            colour=discord.Colour.green())
        embed.set_author(
            name=interactions.user,
            icon_url=interactions.user.avatar)
        await interactions.response.send_message(embed=embed)


class viperarpg(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')

    @discord.slash_command(name='testmodal', description='An example modal')
    async def modal(ctx, interactions: Interaction):
        await interactions.response.send_modal(my_modal())

    @discord.slash_command(name='rps', description='Rock, Paper Scissors')
    @discord.option(name='choice',choices=[
        discord.OptionChoice(name="Rock", value="Rock"),
        discord.OptionChoice(name="Paper", value="Paper"),
        discord.OptionChoice(name="Scissors", value="Scissors"),
    ])
    async def rps(self, interactions: Interaction, choices):
        if (choices.value == 'Rock'):
            counter = 'Paper'
        elif (choices.value == 'Paper'):
            counter = 'Scissors'
        else:
            counter = 'Rock'
        message = (f'I play {counter}, you played {choices.value}. I win!!')
        await interactions.response.send_message(message)

    @discord.slash_command(name='rpg', description='Prints current user info')
    async def rpg(ctx, interactions: Interaction):
        print(interactions.user.id)
        if interactions.user.id == 161612500981252096:
            embed = discord.Embed(
                title='SCID',
                url='https://robertsspaceindustries.com/citizens/SCID',
                timestamp=datetime.now(),
                colour=discord.Colour.dark_green(),
                description='PewPew Killer, PVP Queen, Vipera Veil Leader'
            )
            embed.set_thumbnail(
                # url='https://robertsspaceindustries.com/media/eonii7j69hljqr/heap_infobox/SNEK-Logo.png'
                url='https://robertsspaceindustries.com/media/eonii7j69hljqr/heap_infobox/SNEK-Logo.png'
            )
            embed.set_image(
                url='https://robertsspaceindustries.com/media/obnmucxta7it2r/heap_infobox/IMG_3463.jpg')
            embed.set_footer(
                text=interactions.user.name,
                icon_url=interactions.user.display_avatar
                # url='https://robertsspaceindustries.com/citizens/the_Gunner'
            )
            embed.add_field(
                name='Type:',
                value='Pilot',
                inline=False
            )
            embed.add_field(
                name='Organization:',
                value='[Vipera Veil](https://robertsspaceindustries.com/orgs/SNEK)',
                inline=False)
            embed.add_field(
                name='Stats:',
                value='HP: 6969 \nTask Speed: 🔸🔸\nBlood Lust:🔸🔸🔸🔹🔹\nSurvivability: 🔸🔸🔹\nRamming: 🔸🔸🔸🔹🔹',
                inline=False)
            embed.add_field(
                name='Leaderboard rank:',
                value='N/A',
                inline=False
            )
            embed.add_field(
                name='Important Achievements:',
                value='🥉 AtmoEsports Tobii Clash',
                inline=False
            )
            embed.add_field(
                name='Quote:',
                value='“Hiss Hiss Motherfker“',
                inline=False
            )
            await interactions.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(viperarpg(bot))
