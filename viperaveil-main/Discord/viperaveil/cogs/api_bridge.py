"""
API Bridge events cog
"""
import logging
import discord
import requests
import xml.etree.ElementTree as ET
from discord.ext import commands, tasks
from viperaveil.utilities.Constants import YT_API_TOPICS

logger = logging.getLogger('discord')

endpoints = ['yt_webhook']

async def yt_update(self, content, context):
    guild: discord.Guild = self.bot.get_guild(303245408539246603) # testing_guild = 643051006782996491, prod_guild = 303245408539246603
    if context=='org':
        channel: discord.TextChannel = guild.get_channel(998786333378093056) # testing_channel = 643072384001114112, testing_vipera_channel = 1018444002883797013, prod_channel = 998786333378093056
        at_role = "<@&1096189578689380432>"
    elif context=='gabs':
        channel: discord.TextChannel = guild.get_channel(435861929844801536)
        at_role = "<@&1013206371648413717>"
    # details_embed = discord.Embed(
    #     title=content
    # )
    #await channel.send(embed=details_embed)
    await channel.send(f"{at_role}\nhttps://youtu.be/{content['video_id']}\n{content['title']}")

class APIBridge(commands.Cog):
    """
    Class for api bridge
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')
        self.bot.event_loop_list = []

        APIBridge.var_event_loop.start(self)
        APIBridge.post_yt_sub_update.start(self)

    @tasks.loop(seconds=1.0)
    async def var_event_loop(self):
        #print('Event loop length: ' + str(len(self.bot.event_loop_list)))
        for entry in self.bot.event_loop_list:
            data = f"Endpoint: {entry[0]}, Payload: {entry[1]}"
            await self.bot.get_guild(303245408539246603).get_channel(435861929844801536).send(content=data)
            if entry[0] in endpoints:
                #print('Endpoint - ' + entry[0] + ', Payload - ' + entry[1])
                if entry[0] == 'yt_webhook':
                    root = ET.fromstring(entry[1])
                    channel_id = root.find('.//{http://www.youtube.com/xml/schemas/2015}channelId').text
                    channel_check = next((item for item in YT_API_TOPICS if item[0] == channel_id), None)
                    if channel_check:

                        video_id = root.find(".//{http://www.youtube.com/xml/schemas/2015}videoId").text
                        title = root.find(".//{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}title").text
                        content = {}
                        content['title'] = title
                        content['video_id'] = video_id

                        await yt_update(self, content=content, context=channel_check[1])
                self.bot.event_loop_list.remove(entry)
            else:
                print('Incorrect endpoint: ' + entry[0])
                self.bot.event_loop_list.remove(entry)

    @tasks.loop(hours=24)
    async def post_yt_sub_update(self):
        for topics in YT_API_TOPICS:
            r = requests.post(f'https://pubsubhubbub.appspot.com/subscribe?hub.mode=subscribe&hub.topic=https://www.youtube.com/xml/feeds/videos.xml?channel_id={topics[0]}&hub.callback=https://www.viperaveil.net/api/webhooks/youtube&hub.verify=sync')
            print('Updated yt sub, response: ' + str(r.status_code))
            print(r.text)

def setup(bot):
    """Imports Cog class on class import"""
    bot.add_cog(APIBridge(bot))
