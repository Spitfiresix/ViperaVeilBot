import discord
from datetime import datetime
from viperaveil.lib.cogs.api import apiRSILookup
from viperaveil.utilities.ApiCalls import GetRSIUser
import logging
logger = logging.getLogger('discord')


async def RSILookup(self, ctx: discord.Interaction, scusername: str, auto_delete: bool = False, with_send: bool = True):
    async with ctx.channel.typing():
        # Validating account existence
        playerData = GetRSIUser(scusername)
        if not type(playerData) == dict:
            playerData = 'Player does not exist'
        # playerData = apiRSILookup(scusername, 'user')
        if playerData == 'Player does not exist':
            if with_send == True:
                await ctx.response.send_message(embed=discord.Embed(title='Error! Username does not exist, please recheck it', colour=discord.Colour.red()), ephemeral=True, delete_after=12)
                return
            else:
                return discord.Embed(title=f"{scusername} does not exist")

        if playerData['data']['profile']['handle'] in [
                'the_Gunner', 'SpitfireSix', 'PdxTaz']:
            playerData['data']['profile']['badge'] = 'Booty Hunter'
            playerData['data']['profile']['badge_image'] = 'https://cdn.discordapp.com/attachments/1030028615561261056/1049164237680934912/image.png'
        if playerData['data']['profile']['handle'] in ['StreamerName']:
            playerData['data']['profile']['badge'] = 'Queen of Pyro'
            playerData['data']['profile']['badge_image'] = 'https://cdn.discordapp.com/emojis/969784973156569148.gif?size=96&quality=lossless'

        cachedData = False
        if playerData['source'] == 'cache':
            cachedData = True
        playerProfile = playerData['data']['profile']
        fluency = playerProfile['fluency']

        # Checking if user is actually in an org before calling further info
        orgFound = False
        if playerData['data'].get('organization'):
            if playerData['data']['organization'].get('sid') is not None:
                orgData = playerData['data']['organization']
                orgMemTot = playerData['data']['organization']['members']
                # Pulling org info

                stars_active = ('<:orgsrankactive:1145126212306472990>' * int(playerData['data']['profile']['stars']))
                stars_inactive = ('<:orgsrankinactive:1145126236406956052>' * (5 - int(playerData['data']['profile']['stars'])))
                stars_total = stars_active + stars_inactive
                orgMemPlayerOrg = f'{playerData["data"]["profile"]["rank"]} [{stars_total}] @ [{orgData["name"]}](https://robertsspaceindustries.com/orgs/{orgData["sid"]}) [{orgMemTot} Members]'
                #orgMemPlayerOrg = f'{playerData["data"]["profile"]["rank"]} [{playerData["data"]["profile"]["stars"]}] @ [{orgData["name"]}](https://robertsspaceindustries.com/orgs/{orgData["sid"]}) [{orgMemTot} Members]'
                orgFound = True
        # No org so content = None
        if not orgFound:
            orgMemPlayerOrg = 'Player is not a member of any org'

        playerWebsite = playerProfile.get('website')

        # Building embed to push to Discord
        detailsEmbed = discord.Embed(
            title=f'{playerProfile["handle"]} | {playerProfile["display"]}',
            url=f'https://robertsspaceindustries.com/citizens/{playerProfile["handle"]}',
            timestamp=datetime.now(),
            colour=discord.Colour.dark_green(),
            description=playerProfile['recordID'])
        # Top left text and badge
        detailsEmbed.set_author(
            name=playerProfile["badge"],
            icon_url=playerProfile["badge_image"])
        detailsEmbed.set_thumbnail(
            url=playerProfile['image']
        )
        # Account creation date, in user friendly format
        detailsEmbed.add_field(
            name='Enlisted',
            value=f'{(datetime.strptime(playerProfile["enlisted"],"%Y-%m-%d %H:%M:%S")).strftime("%b %d, %Y")}',
            inline=True)
        # Language list, pulled from above
        detailsEmbed.add_field(
            name='Languages',
            value=fluency,
            inline=True
        )
        # Website, pulled from above
        detailsEmbed.add_field(
            name='Website',
            value=playerWebsite,
            inline=True
        )
        # Main org, mix of literal strings and variables from above
        detailsEmbed.add_field(
            name='Main Org',
            value=orgMemPlayerOrg,
            inline=False
        )
        if cachedData is True:
            detailsEmbed.add_field(
                name='‎\nUsing Cache',
                value='Profile retrieved from cache',
                inline=False
            )
        else:
            detailsEmbed.add_field(
                name='‎\nLive Data',
                value='Cache outdated, pulling live',
                inline=False
            )
        # Contains info about the Discord user that called this event and the
        # datetime for it
        detailsEmbed.set_footer(
            text=ctx.user.name,
            icon_url=ctx.user.display_avatar
        )
        if with_send == True:
            if auto_delete == False:
                await ctx.response.send_message(embeds=[detailsEmbed])
            else:
                await ctx.response.send_message(embeds=[detailsEmbed], delete_after=30)
        else:
            return detailsEmbed
