import discord
from viperaveil.utilities.Constants import snekLogoRegular, VENM_LOGO


def viperaInfoEmbed():
    vipera_embed = discord.Embed(
        title='Vipera Veil 🐍',
        colour=discord.Colour.dark_green(),
        url='https://robertsspaceindustries.com/orgs/SNEK',
        description="""
Vipera Veil is an exclusive group of competitive badasses focused on PVP, within our team culture we not only create an organization but create a lifelong bond and family.
‎
We are looking for competitive Pilots, FPS Forces & Specialists.
We value devotion, loyalty, respect, positivity, trustworthiness, knowledge of the game, good humor, and a will to improve. 
‎
We can offer you team coordination, focused trainings with the best pvpers in the game, lots of w's, weekly events vs pvp orgs, promotion in our social media, karaoke fps team, drunk nights, dcs nights, one (1) gamer girl, movie nights & you get to waste a lot of money buying a different game every day 🙂 (just kidding).
‎
Are you a competitive PVPer? Ready to pledge your loyalty to the Vipera Veil.? [Apply here!](https://docs.google.com/forms/d/1LxUCxttxNMq6EpDk2mbgsj4_Td1aVYJAHPAXqcana9k/edit)"""
    )
    vipera_embed.set_thumbnail(
        url=snekLogoRegular
    )
#     vipera_embed.add_field(
#         name="""‎""",
#         value="""
# > **We are looking for:**
# > • Devotion to the group
# > • Loyalty
# > • Respect
# > • Positivity
# > • Trustworthy individuals
# > • Knowledge of the game
# > • Good humor
# > • Will to get better/improve\n‎
# We are the competitive clan of warriors following the traditions of the Mandalorian from the Star Wars universe. within our team culture we follow the creed to not only create a organization but to create a lifelong bond and family. \n""",
#         inline=False
#     )
#     vipera_embed.add_field(
#         name="""‎""",
#         value="""> ***<:gabizMando:1011349931195375756> The Creed.***
# > *Strength is life
# > for the strong will have the right to rule
# > honor is life for with no honor one may as well be dead
# > loyalty is life
# > for without ones clan, one has no purpose
# > death is life
# > one should die as they lived.*\n‎""",
#         inline=False
#     )
#     vipera_embed.add_field(
#         name="""🚀 Pilots""",
#         value="We are looking for team focused pilots who want to sharpen their skills and learn to fight as one. The correct attitude is the most important. If you bring a willingness to learn, we will teach you the way.",
#         inline=False
#     )
#     vipera_embed.add_field(
#         name="🔫 FPS",
#         value="We are looking for people who work well solo, but also are willing to work as a team for target exploitation and infiltration. Proper attitude and a growth mindset required.",
#         inline=False
#     )
#     vipera_embed.add_field(
#         name="🏎️ Specialists ⛏️",
#         value="We also welcome players who want to explore other aspects of Star Citizen. Anything from mining and hauling to low flying.",
#         inline=False)
#     vipera_embed.add_field(
#         name="""‎""",
#         value="""> Are you a competitive PVPer? Or want to be one? Apply [here](https://forms.gle/uipQraSdtYSFP72y7)!""",
#         inline=False)
    venom_embed = discord.Embed(
        title='Venom Squadron 🐍',
        colour=discord.Colour.dark_orange(),
        url='https://robertsspaceindustries.com/orgs/VNMSQD/',
        description="""
Venom Squadron is a Vipera Veil Squadron that is open to all players of all levels. Venom is non-exclusive, so you can be a part of Venom Squadron while also being a member of other organizations. We will be hosting events, tournaments, and other activities to bring our members together and help them improve their skills and enjoy their favorite game even more.
‎
Pilots, FPS Forces, Miners, Racers, Specialists & more are welcome to join!
‎
Go to [RSI VNMSQD](https://robertsspaceindustries.com/orgs/VNMSQD) and click "Join Us Now".
Once you've received an invite go to: [RSI Org Invites](https://robertsspaceindustries.com/account/organization/invitations) and accept the invitation.
Ping <@161612500981252096> or <@&452288214607331328> to get the Venom role tag or verify your RSI account here ⁠[RSI Verify](https://discord.com/channels/303245408539246603/1120444881383465033)
"""
    )
    venom_embed.set_thumbnail(
        url=VENM_LOGO
    )
    return [vipera_embed, venom_embed]


def gabsInfoEmbed():
    detailsEmbed = discord.Embed(
        title='✨ Violinist 🎻 Streamer 👾',
        url='https://discord.gg/gabiz',
        colour=discord.Colour.purple(),
        description="""<a:JAMMIES:896697664752742450> **[Website](https://missgabiz.com/)**

I'm Gabi, I am majoring in classical music/violin performance.
I mostly PVP on Star Citizen and love creating content.
I'm also a huge star wars nerd.

<a:02Hype:1006174782351495278> **Direct business line** -> gabizbusiness@gmail.com\n ‎ """)
    # detailsEmbed.set_author(name=interactions.user.name, icon_url='https://robertsspaceindustries.com/media/eonii7j69hljqr/logo/SNEK-Logo.png')
    detailsEmbed.set_thumbnail(
        url='https://cdn.beacons.ai/user_content/jk4BTjlJvcY9KbtCzOn9fsWdYeF3/profile_missgabiz.png')
    detailsEmbed.add_field(
        name='⋆ ˚｡⋆୨୧˚ SOCIALS ˚୨୧⋆｡˚ ⋆',
        value="""I often post updates in all my socials. Check them out to stay updated.\n
> <:gabizWow:941457217364848680> **[Twitch](https://www.twitch.tv/missgabiz)**
> <:gabizPico:1011349824819433523> **[YouTube](https://www.youtube.com/@missgabiz)**
> <:gabizPilotsw:1011349607726452776> **[Twiter](https://twitter.com/missgabiz)**
> <a:gabizLurk1:1002870252574617611> **[Exclusive Content](https://fansly.com/missgabiz)**
> <:gabizSmug:941457952320139285> **[Tiktok](https://www.tiktok.com/@missgabiz)**
> <:gabizCool:941456656095641680> **[Instagram](https://www.instagram.com/missgabiz_)**
> <a:gabizTea:948287456044785734> **[Gabiz Clips Youtube](https://youtube.com/@gabizclips)**
> <:gabizHungry:1011349877172748338> **[Gabiz ASMR Youtube](https://youtube.com/@gabizasmr)**
> <a:gabizPilot:948287406694613062> **[Gear](https://throne.me/missgabiz/storefront)**\n‎ """,
        inline=False)
    detailsEmbed.add_field(
        name='⋆ ˚｡⋆୨୧˚ SUPPORT ˚୨୧⋆｡˚ ⋆',
        value="""Thank you so much for supporting me more! Donations or gifts goes towards improving the stream but aren't necessary!
I'm happy just to have you here but anything is greatly appreciated.

> **<a:gabizComfy1:1002870198690381824> [My wishlist](https://throne.me/u/missgabiz/wishlist)**
> **<a:gabizWiggle:986703696278720542> [Donate](<https://streamelements.com/missgabiz/tip)**
> **<:gabizSocks:941457153888256020>[Merch Store](https://gabizmerch-shop.fourthwall.com)**

Please use the code 'missgabiz' for a 5% off. You help my content a lot by using my code! Thank you so much <:gabizHeart:1011349778023579698>

<:gabizMando:1011349931195375756> [Tobii Eye Tracker](https://tobii.gg/missgabiz)
<:gabizPilotsw:1011349607726452776> Monstertech [USA](https://www.monstertechusa.com/)/[Global](https://www.monster.tech/en/)""",
        inline=False)
    detailsEmbed.add_field(
        name='‎',
        value="""No words can describe how thankful I am to have so many amazing people in my life. I'm so lucky to have you guys, I don't know what I did to deserve this. Thank you, thank you so much for all your support. I love you guys, please stay wholesome ;-; ❤️""",
        inline=False
    )
    detailsEmbed.add_field(
        name='‎',
        value='If you want access to some **exclusive** channels, follow the steps below:',
        inline=False
    )
    detailsEmbed.set_image(url='https://www.viperaveil.net/static/images/discord/howtoconnect.png')
    return detailsEmbed


def viperaEventLeaderboard():
    detailsEmbed = discord.Embed(
        title='🏆 EVENT LEADERBOARD 🏆',
        url='https://discord.gg/gabiz',
        colour=discord.Colour.dark_green(),
        description='[Vipera Veil](https://robertsspaceindustries.com/orgs/SNEK)')
    # detailsEmbed.set_author(name=interactions.user.name, icon_url='https://robertsspaceindustries.com/media/eonii7j69hljqr/logo/SNEK-Logo.png')
    detailsEmbed.set_thumbnail(
        url='https://robertsspaceindustries.com/media/eonii7j69hljqr/logo/SNEK-Logo.png')
    detailsEmbed.add_field(
        name='AtmoEsports FoF',
        value='🥇 ErektPigeon & Witcher (Black Fleet)',
        inline=False
    )
    detailsEmbed.add_field(
        name='4vs4 Asteroid Crashers Tournament',
        value="🥇 Liberty's Reapers 🥈 🥉 ",
        inline=False
    )
    detailsEmbed.add_field(
        name='SPK FPS Battle #1',
        value='🥇 Tie: Vipera Veil & BlackFleet',
        inline=False
    )
    detailsEmbed.add_field(
        name='SPK FPS Battle #2',
        value='🥇 Avenger Squadron',
        inline=False
    )
    detailsEmbed.add_field(
        name='AtmoEsports Tobii Clash',
        value='🥇 AvengerOne 🥈 XeroState 🥉 MissGabiz',
        inline=False
    )
    detailsEmbed.add_field(
        name='50vs50',
        value='🥇Team Vipera Veil, R4M Department, BLK, SKUNKWORKS',
        inline=False
    )
    detailsEmbed.add_field(
        name='100 FFA',
        value='🥇Xiaojuna 🥈 Syllytime 🥉 Sony_USR',
        inline=False
    )
    detailsEmbed.add_field(
        name='New Years Party',
        value='🥇BSI Thunderlake & Japhero3',
        inline=False
    )
    return detailsEmbed

def viperaRanksEmbed():
    detailsEmbed = discord.Embed(
        title='Structure',
        colour=discord.Colour.dark_green(),
        url='https://robertsspaceindustries.com/orgs/SNEK',
    )
    detailsEmbed.set_thumbnail(
        url=snekLogoRegular
    )
    detailsEmbed.add_field(name='__**Org Ranks:**__', value="""
    > **Family Leader:** The leader of a single clan. Only one individual holds this position. You sit on top of the food chain of your clan. You need not to seek of honor for it is you who create it.
    > **Council:** The ones in charge of expansion, politics, diplomacy, events etc.""", inline=False)
    detailsEmbed.add_field(name='__**Org Roles:**__', value='‎', inline=False)
    #     detailsEmbed.add_field(
    #         name="""‎""",
    #         value="""
    # > **Captain:** The second officer rank and leader of a standard class SNEKs. At the rank of Captain you are a senior to those who boast of being SNEKs as you know the only real proof of skill and power is through combat. You are naturally an "alpha" being with the ability to collectively lead a group of "wild dogs." Very few are given this title.""",
    #         inline=False
    #     )
    #     detailsEmbed.add_field(
    #         name="""‎""",
    #         value="""
    # > **Lieutenant:** The first officer rank. The highest rank for special trained SNEKs. The rank of Lieutenant serves as the front line leader.""",
    #         inline=False
    #     )
    #     detailsEmbed.add_field(
    #         name="""‎""",
    #         value="""
    # > **Sergeant:** Experienced and loyal to the family. Time and time again, you earn your keep. You have built quite a reputation for yourself...a little too unanimously.""",
    #         inline=False
    #     )
    #     detailsEmbed.add_field(
    #         name="""‎""",
    #         value="""
    # > **Warrior:** This is the first actual showing of proof as a full fledged family warrior. Honor has been tested and paid by blood. The thrill of the fight has been tasted and the fruition for more has just begun. You know it's necessary to stay witty and vigilant even at rest.""",
    #         inline=False
    #     )
    #     detailsEmbed.add_field(
    #         name="""‎""",
    #         value="""
    # > **Prospect:** When the common man is initiated into a clan and branded as a true warrior worthy of the family name. Not holding any status beyond that.""",
    #         inline=False
    #     )
    #     detailsEmbed.add_field(name="""‎
    # **Roles:**""", value='‎', inline=False)
    detailsEmbed.add_field(
            name="""‎""",
            value="""
> **War Leader:** The role of War Leader serves as the front line leader of the SNEKS in their specific path (Viper, Cobra or Python)

- Viper Leader
- Cobra Leader
- Python Leader
- Dropship Leader
- Flight Instructor
- FPS Instructor
- ACE (Made it to top 50 on AC leader boards)
- Ranger (Made it to top 50 on SM leader boards)
- Analyst

> **Warrior:** This is the first actual showing of proof as a full fledged family warrior. Honor has been tested and paid by blood. The thrill of the fight has been tasted and the fruition for more has just begun. You know it's necessary to stay witty and vigilant even at rest.

> **Prospect:** When the common man is initiated into a clan and branded as a true warrior worthy of the family name. Not holding any status beyond that.
    """,
            inline=False
        )
    detailsEmbed.add_field(
        name="""\n__**Path Structure:**__""",
        value="""‎""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""**Pilot Force:**""",
        value="""**Mascot:** Viper
The most vital and mobile branch of the SNEKs. The fighter pilots are often based on light fighters and seek to compete in tournaments and competitive events.""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""**Viper Ranks:**
> **Tier 1** - Learn Comms 
> **Tier 2** - Kill someone in top 150 on Leader board 
> **Tier 3** - Kill someone in top 30 on Leader Board""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""**Assault Force:**""",
        value="""**Mascot:** Cobra
Composed of a strictly assault squadron. The largest element of Cobra is a troop which is a collection of assaulters who can break into smaller teams. The troop must be able to perform the core tasks mentioned below. Core Missions for A cobra troop, Direct Action Raids, Special Reconnaissance, Hostage Rescue, EVA operations, Ambush.""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""**Cobra Ranks:**
> **Tier 1** - Candidate 
> **Tier 2** - Passed The escape and evasion event
> **Tier 3** - Successful deployment of Jumptown and has master at minimum 1 of the core operator skills""",
        inline=False
    )
    detailsEmbed.add_field(
        name='Core Operator Skills:',
        value="""Breacher
Sniper
JTAC
Corpsman/Medical Specialist
Navigator/Point man,
Heavy Weapons Operator
Lead EVA ,
Surveillance
Tank Commander
Target Exploitation""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""**Special Activities:**""",
        value="""**Mascot:** Python
Special activities unit, is a collection of highly trained specialist that can perform required functions to support. It consists of primarily the best drop ship pilots in the star citizen universe.""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""**Python Ranks:**
> **Tier 1**
> **Tier 2**
> **Tier 3**""",
        inline=False
    )
    detailsEmbed.add_field(
        name='**Core Skills:**',
        value="""Dropship Hot Extract/Infil
Strategic Bomber 
Ship Interdiction 
Close Air Support 
Ariel Intelligence""",
        inline=False
    )
    #     detailsEmbed.add_field(
    #         name="""‎""",
    #         value="""
    # > **Warrior of the Shadows:** TBD""",
    #         inline=False
    #     )
    #detailsEmbed.add_field(name='**Path Structure:**', value='‎', inline=False)

    return detailsEmbed

def viperaStandardsEmbed():
    detailsEmbed = discord.Embed(
        title='What we expect of you',
        colour=discord.Colour.dark_green(),
        url='https://robertsspaceindustries.com/orgs/SNEK',
    )
    detailsEmbed.set_thumbnail(
        url=snekLogoRegular
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 1. Respect all members of the org, regardless of their rank or skill level.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 2. All members must be dedicated to the goals and values of the org.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 3. Members must not disclose any confidential information about the org to outsiders (stuff we say in the org channels).
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 4. All members must work to uphold the reputation of the org at all times.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 5. Do not engage in any form of harassment or bullying within the org or towards other players.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 6. Assist the org with promotion. Make sure you have shadow replay installed, set it to a minimum of 30secs-1min and clip every kill you get in Arena Commander, PU/PTU, or Star Marine. We only need the splashes to make a promotional video, we don’t need 1 hour recordings. You are also required to clip the kills of PVP org events we do or join. You can also clip any in-game activities, events or just hanging out and having fun with your teammates.
> We do NOT need to remind you to do this every single event, please remember to do it. We will use these clips to attract new members and show the community the great organization we have built.
> If you have any footage that you think would be suitable, please submit it to the designated folders (our shared [google drive](https://drive.google.com/drive/folders/1OeEj1uIrpBMl6cNZxelaKv5TB7LbSrui?usp=share_link) or <#1066990079098241084> ) Thank you for your support and let's continue to build our amazing org together!
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 7. Do not cheat or exploit any bugs in the game.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 8. Do not use racial, ethnic, or offensive language on Star Citizen discords/websites or in game, how you act is a reflection of the org and who we are. **Watch your behavior.**
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 9. All members must respect the decisions or instructions of the leaders and captains at all times.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 10. Members are encouraged to bring any concerns or issues to the attention of leadership in a respectful and constructive manner.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 11. Be active and participate in org events and activities, and assist fellow members when needed.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 12. Discord lets you edit your server profile without changing your whole discord profile. Please make sure on Star Citizen discords you edit your server profile and add the [SNEK] tag and profile banner.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 13. Any type of recruiting is appreciated, feel free to DM people you fight in Arena Commander, Star Marine, PU/PTU letting them know about the org.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 14. No infiltration allowed unless explicitly authorized by the Council members.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 15. Any member found to be working against the interests of the org will be subject to disciplinary action.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 16. Any form of betrayal or disloyalty will not be tolerated and will result in immediate expulsion from the org.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
> 17. Any member found to be undermining the org in any way will be subject to disciplinary action up to and including expulsion.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
As a reminder, all members must abide by the standards set forth by the org. Any violations of these rules will not be tolerated and will result in disciplinary action.
A three-strike system will be implemented for rule violations. After a member receives three strikes, they will be demoted to a lower rank within the org.
Please understand that this decision has been made in the best interest of maintaining a positive and productive environment for all members. We ask for your cooperation in adhering to the rules and helping to create a strong and successful org.
If you have any questions or concerns, please reach out to the Council.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
We understand that it can be easy to forget the standards and expectations that have been set forth for our org. However, it is important to always keep these things in mind and strive to uphold them in our actions and interactions.
As a reminder, please take the time to review the standards and make sure you understand and are adhering to them. It is not only important for the overall success and unity of our org, but also for the fair treatment and respect of all members.
We kindly ask that you refrain from asking for reminders and reiterations of the standards on a regular basis. Instead, please take responsibility for familiarizing yourself and staying up-to-date with them.
""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""
Let's work together to create and maintain a positive and productive environment for all members.
If you have any questions or concerns, please reach out to the Council.
""",
        inline=False
    )
    return detailsEmbed

def viperaLinksEmbed():
    detailsEmbed = discord.Embed(
        title='Useful Links',
        colour=discord.Colour.dark_green(),
        url='https://robertsspaceindustries.com/orgs/SNEK',
        description="""
[Org Docs](https://drive.google.com/drive/folders/10xsMQCb_O2GvLRg4euIL4th-6TtfiVxt?usp=sharing)
You can find all our team tactics and important documents here, you also have a drop org videos folder to upload your clips for org promotion. If you are a full member and cannot access the channel, please send me your email to have access to the drive.

[Org's Calendar](https://calendar.google.com/calendar/u/3?cid=dmlwZXJhdmVpbEBnbWFpbC5jb20)"""
    )
    detailsEmbed.set_thumbnail(
        url=snekLogoRegular
    )
    return detailsEmbed

def viperaSnekWarsEmbed():
    detailsEmbed = discord.Embed(
        title='Snek Wars 🐍',
        colour=discord.Colour.dark_green(),
        url='https://robertsspaceindustries.com/orgs/SNEK',
        description="""‎"""
    )
    detailsEmbed.set_thumbnail(
        url=snekLogoRegular
    )
  
    detailsEmbed.add_field(
        name="""‎""",
        value="""***Introduction***
> SNEK WARS is a Tool Developed by Vipera Veil that allows us, the PvP community, to engage in
> skilled combat with each other regularly. It is essentially a Pickup Server designed for Star
> Citizen, a venue where we gather, join lobbies, pick teams, and go brawl. This is like Dodgeball
> with Light Fighters.
‎""",
        inline=False
    )
    detailsEmbed.add_field(
        name="""‎""",
        value="""***What are Pickups ***
> Pickups are a style of competitive practice where 2 teams are selected at random, or by Team
> Captain Style picking similar to dodgeball. Teams are picked, then you play. Think of it like
> unlimited Back to Back Scrims, anytime & anyplace, but you will play with and against all types
> of Pilots from Various Orgs Competitive and maybe Casual Players Alike.
‎""",
        inline=False
    )

    detailsEmbed.add_field(
        name="""‎""",
        value="""***The Benefits***
> Pickup Servers are massively common on FPS competitive Games, when the Comp
> scene is stale and activity waivers where do players go that still have that itch to
> compete at a high level? Pickups…
> When the Game itself fails to provide adequate mechanics for healthy PvP like NO
> private Lobbies, where do the sweaties go? Pickups…
> When you Join a Competitive Org, and you need to Improve your skills in the best way
> possible? Go to Pickups…
‎
> You will get to Learn from, Fight Alongside, and Against the Toughest Pilots on Star
> Citizen. HOW? Because one thing is historically accurate in Competitive Gaming. The
> Best Players are the most addicted to Playing at a High Level, ALOT. And the one place
> to get that Level of Action 24/7 will be
> right here, In **SNEK WARS**
‎""",
        inline=False
    )
    return detailsEmbed

async def viperaPickupEmbed(self, _queue = ''):
    current_queue = {}
    current_queue['1v1'] = []
    current_queue['2v2'] = []
    current_queue['3v3'] = []
    current_queue['4v4'] = []
    if _queue == '':
        _queue = {}
        _queue['1v1'] = []
        _queue['2v2'] = []
        _queue['3v3'] = []
        _queue['4v4'] = []
    else:
        for types in _queue:
            for player in _queue[types]:
                player_tag = await self.bot.get_or_fetch_user(player[0])
                current_queue[types].append(player_tag.mention)

    detailsEmbed = discord.Embed(
    title='__SNEK WARS__',
    colour=discord.Colour.dark_green(),
    description='[**Read the Rules!**](https://discord.com/channels/303245408539246603/1074877620082184284)'
    )
    detailsEmbed.set_thumbnail(url='https://www.viperaveil.net/static/images/logo512.png')
    detailsEmbed.add_field(
        name='**Queues**',
        value='‎',
        inline=False
    )
    for types in current_queue:
        if len(current_queue[types]) == 0:
            current_queue_string = 'Empty'
        else:
            current_queue_string = ''
            for players in current_queue[types]:
                current_queue_string += players + '\n'
        if types == '3v3':
            detailsEmbed.add_field(
                name='‎',
                value='‎',
                inline=False
            )
        detailsEmbed.add_field(
            name=types,
            value=current_queue_string,
            inline=True
        )
    return detailsEmbed

def vipera_ticket(self):
    title = '🚀 Flight School & FPS School🔫'
    embed = discord.Embed(
        title=title, colour=discord.Colour.dark_green())
    # embed.add_field(name="🚀 Flight School", value="""Want PVP Flight Lessons? :rocket:
    # This will open a training request with our Flight Instructors!
    # Make sure when you open the request you are ready to go!
    # **Have a Gladius or Arrow ready to go!**""", inline=True)
    # embed.add_field(name="🔫 FPS School", value="""Want FPS lessons? 🔫
    # This will open a training request with our FPS Instructors!
    # Make sure when you open the request you are ready to go!""",
    # inline=True)
    embed.add_field(
        name='Want PVP Flight or FPS Lessons? 🚀',
        value="""This will open a training request with our Instructors!\n Our lessons are 1 on 1, you can schedule the training session!""")
    embed.set_thumbnail(url=snekLogoRegular)
    embed.set_author(name=self.bot.user.name)
    return embed