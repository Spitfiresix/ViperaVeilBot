import os
import json
import logging
import logging.handlers
from typing import List

import tekore
from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sclib.asyncio import SoundcloudAPI

import discord
from discord.ext import commands

from viperasnek.utilities.database.Connection import db_connection

dir_path = os.path.dirname(os.path.realpath(__file__))

DEV_CONFIG_FILEPATH = 'viperasnek/configurationtesting.json'
PROD_CONFIG_FILEPATH = 'viperasnek/configuration.json'
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

spotify_client_id = data["spotifyClientId"]
spotify_client_secret = data["spotifyClientSecret"]
dbl_token = data["dblToken"]

intents = discord.Intents.all()

CogList = []
for filename in os.listdir("./viperasnek/cogs"):
    if filename.endswith(".py"):
        CogList.append(f"viperasnek.cogs.{filename[:-3]}")

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

class ViperaSNEK(commands.AutoShardedBot): # pylint: disable=too-few-public-methods,too-many-instance-attributes
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
        # Help
        # self.remove_command("help")
        # ^^ To create a personal help command
        # Database
        self.db_connection = db_connection()
        for extension in initial_extensions:
            self.load_extension(extension)


async def main(token):
    """
    Initialize and launch bot class
    """
    print('Starting Vipera SNEK Discord Worker')
    logger = logging.getLogger('discord')

    if os.environ.get('DEBUG_MODE') == 'True':
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(
        '[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    engine = create_async_engine(DB_URL, echo=False)

    async with engine.connect() as conn:
        bot = ViperaSNEK(commands.when_mentioned,
                             session=conn,
                             initial_extensions=CogList)
        await bot.start(token, reconnect=True)
        