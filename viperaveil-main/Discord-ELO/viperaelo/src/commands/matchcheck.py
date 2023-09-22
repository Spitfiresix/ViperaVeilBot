import discord
import random
from discord import Embed
from discord.ext import commands
import time
import json
import requests
from src.utils.constants import getBaseUrlEndpoint

# Class watches the match cache 
class MatchCheckCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_base_url = f"{getBaseUrlEndpoint()}/api/matchmaking"  # Replace with the actual base URL of your API

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")
        self.bot.loop.create_task(self.match_check_loop())

    async def check_has_match(self):
        has_match_url = f"{self.api_base_url}/has-match"
        response = requests.get(has_match_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    async def get_match(self):
        get_match_url = f"{self.api_base_url}/get-match"
        response = requests.get(get_match_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def deserialize_match(self, match_json):
        # Add your custom deserialization logic here
        match_data = json.loads(match_json)
        return match_data

    def process_match(self, match_data):
        # Add your custom processing logic here
        print("Match found!")
        print(match_data)
        # ...

    async def match_check_loop(self):
        while True:
            has_match = await self.check_has_match()
            if has_match:
                match = await self.get_match()
                if match:
                    match_data = self.deserialize_match(match)
                    self.process_match(match_data)
            time.sleep(5)
