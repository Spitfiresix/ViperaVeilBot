"""
Vipera Veil Bot Main Class Generator
"""

# Letssss gooooo
# Gunner#1337
# Importing modules
# Note, that any that haven't been added to requirements.txt need to be
# built in to Python
import os
import json
import logging
import logging.handlers
import asyncio

from typing import List, Optional

# Spotify
import tekore
from aiohttp import ClientSession
from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sclib.asyncio import SoundcloudAPI

import discord
from discord.ext import commands

from viperaveil.lib.database.models import Base, Partial_Register
from viperaveil.utilities.database.Connection import db_connection
from viperaveil.cogs.viperainteractables import viperainteractables
from viperaveil.cogs.viperaticket import TicketEmbedView, OpenTicketEmbedView
from viperaveil.cogs.pick_up_core import pickUpEmbedView

# async with message.channel.typing():
# ^^ This is used further down to simulate 'processing time' with 'typing'
#BOT_TOKEN = os.getenv('TOKEN')
# I don't need to explain this
#discord.utils.setup_logging(level=logging.DEBUG, root=False)

# Setting current location as root for config settings
dir_path = os.path.dirname(os.path.realpath(__file__))

# Or this


def get_prefix(bot, message):
    """
    Gets hard-coded bot prefix
    """

    prefixes = ['$']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'
    # If we are in a guild, we allow for the user to
    # mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


#### Variables/strings...etc ####
# Aliit alor (Gabs), Council, Captains, Members, Prospects.
# Planning to add 'applied' role dependent on Gabs.
snekRoles = ['307763930627833856',
             '1000868850960715931',
             '995924623877226516',
             '995905879637495860',
             '997006295146188930'
             ]
DEV_CONFIG_FILEPATH = 'viperaveil/configurationtesting.json'
PROD_CONFIG_FILEPATH = 'viperaveil/configuration.json'
PROD_POSTGRES_URL = 'postgres-viperaveil.postgres.svc.cluster.local'
DEV_POSTGRES_URL = '10.40.0.80'
POSTGRES_USER = 'viperaveil'
POSTGRES_PW = '7xwlf2r08mhz'
POSTGRES_DB = 'viperaveil'
if os.environ.get('DEBUG_MODE') == 'True':
    print('Running in Development Mode')
    POSTGRES_URL = DEV_POSTGRES_URL
    CONFIG_FILEPATH = DEV_CONFIG_FILEPATH
else:
    print('Running in Production Mode')
    POSTGRES_URL = PROD_POSTGRES_URL
    CONFIG_FILEPATH = PROD_CONFIG_FILEPATH

DB_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}:5434/{POSTGRES_DB}'

with open(CONFIG_FILEPATH, "r", encoding="utf-8") as config:
    data = json.load(config)

token = data["token"]
prefix = data["prefix"]
spotify_client_id = data["spotifyClientId"]
spotify_client_secret = data["spotifyClientSecret"]
dbl_token = data["dblToken"]

with open("viperaveil/emojis.json", "r", encoding="utf-8") as emoji_list_file:
    emoji_list_json = json.load(emoji_list_file)
    emoji_list_data = {
        "YoutubeLogo": emoji_list_json["YouTubeLogo"],
        "SpotifyLogo": emoji_list_json["SpotifyLogo"],
        "SoundcloudLogo": emoji_list_json["SoundCloudLogo"],
        "DeezerLogo": emoji_list_json["DeezerLogo"],
        "True": emoji_list_json["True"],
        "False": emoji_list_json["False"],
        "Alert": emoji_list_json["Alert"]
    }

intents = discord.Intents.all()

CogList = []
for filename in os.listdir("./viperaveil/cogs"):
    if filename.endswith(".py"):
        CogList.append(f"viperaveil.cogs.{filename[:-3]}")


class CreateEmojiList:  # pylint: disable=too-few-public-methods
    """
    Creates emoji list within bot class
    """

    def __init__(self, emoji_list):
        self.youtube_logo = emoji_list["YoutubeLogo"]
        self.spotify_logo = emoji_list["SpotifyLogo"]
        self.soundcloud_logo = emoji_list["SoundcloudLogo"]
        self.deezer_logo = emoji_list["DeezerLogo"]
        self.true = emoji_list["True"]
        self.false = emoji_list["False"]
        self.alert = emoji_list["Alert"]


class CreateLavalink: # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    Create Lavalink variables within bot class
    Used in contructor
    """

    def __init__(self):
        self.host = data["lavalinkHost"]
        self.port = data["lavalinkPort"]
        self.rest_uri = data["lavalinkRestUri"]
        self.password = data["lavalinkPassword"]
        self.identifier = data["lavalinkIdentifier"]
        self.region = data["lavalinkRegion"]
        self.spotify_client_id = data['spotifyClientId']
        self.spotify_client_secret = data['spotifyClientSecret']


class ViperaBot(commands.AutoShardedBot): # pylint: disable=too-few-public-methods,too-many-instance-attributes
    """
    Constructing bot class
    """

    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        session: AsyncEngine,
        # web_client: ClientSession,
        # testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs, intents=discord.Intents.all())
        self.session = session
        # self.web_client = web_client
        # self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
        # Spotify
        spotify_app_token = tekore.request_client_token(
            spotify_client_id, spotify_client_secret)
        self.spotify = tekore.Spotify(spotify_app_token, asynchronous=True)
        # SoundCloud
        self.soundcloud = SoundcloudAPI()
        # Lavalink
        self.lavalink = CreateLavalink()
        # Top.gg
        self.dbl_token = dbl_token
        # Emojis
        self.emoji_list = CreateEmojiList(emoji_list_data)
        # Help
        # self.remove_command("help")
        # ^^ To create a personal help command
        # Database
        self.db_connection = db_connection()
        for extension in initial_extensions:
            self.load_extension(extension)

        # Importing View for persistant loading on bot launch
        self.add_view(viperainteractables.EmbedView(self, self.session))
        self.add_view(TicketEmbedView())
        self.add_view(OpenTicketEmbedView())
        self.add_view(pickUpEmbedView(self))

        if not True:
            if hasattr(self, 'testing_guild_id'):
                guild = discord.Object(self.testing_guild_id)
                # We'll copy in the global commands to test with:
                self.tree.copy_global_to(guild=guild)
                # followed by syncing to the testing guild.
                self.tree.sync(guild=guild)


async def main():
    """
    Initialize and launch bot class
    """

    print('Starting Vipera Veil Discord Connector')
    # logger = logging.getLogger('discord')

    # if os.environ.get('DEBUG_MODE') == 'True':
    #     logger.setLevel(logging.DEBUG)
    # else:
    #     logger.setLevel(logging.INFO)

    # handler = logging.handlers.RotatingFileHandler(
    #     filename='discord.log',
    #     encoding='utf-8',
    #     maxBytes=32 * 1024 * 1024,  # 32 MiB
    #     backupCount=5,  # Rotate through 5 files
    # )
    # dt_fmt = '%Y-%m-%d %H:%M:%S'
    # formatter = logging.Formatter(
    #     '[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)

    engine = create_async_engine(DB_URL, echo=False)
    async with engine.connect() as conn:
        bot = ViperaBot(commands.when_mentioned,
                             session=conn,
                             initial_extensions=CogList)
                             
        await bot.start(token, reconnect=True)