import logging
import discord
from discord.ext import commands
from viperaveil import dir_path
from viperaveil.lib.cogs.rsi.lookup import RSILookup
from PIL import Image, ImageDraw, ImageFont
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes, VisualFeatureTypes
import time

async def processImage(endpoint, apiKey, imageref): 
        #create client
        client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(apiKey))
        #read image
        response = client.read_in_stream(open(imageref, 'rb'),raw=True)
        operationLocation = response.headers['Operation-Location']
        operation_key = operationLocation.split('/')[-1]
        #give time for operation to complete
        time.sleep(5)
        name_list = []
        result = client.get_read_result(operation_key)
        if result.status == OperationStatusCodes.succeeded:
            read_results = result.analyze_result.read_results
            for analyzed_result in read_results:
                for line in analyzed_result.lines:
                    name_list.append(line.text)
        return name_list

logger = logging.getLogger('discord'
                           )
class ViperaImagePlayerLookUp(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')
    
    @commands.guild_only()
    @discord.slash_command(name='imagelookup', 
                           description='paste your image of the name or names you want to look up. Only capture the name')
    async def imagelookup(self, ctx: discord.ApplicationContext, image: discord.Attachment):
        await ctx.defer()
        apiKey= "07da01f0aa604e1492d7c499be793847"
        endpoint="https://viperaveilvision.cognitiveservices.azure.com/"
        user_storage = f'{dir_path}/cache/imagelookup-{ctx.user.id}-{image.filename}'
        await image.save(user_storage)
        user_name_list = await processImage(endpoint, apiKey, user_storage)
        rsi_embeds = []
        for scusername in user_name_list:
            rsi_embeds.append(await RSILookup(self, ctx, scusername, with_send=False))
        await ctx.followup.send(embeds=rsi_embeds)

def setup(bot):
    bot.add_cog(ViperaImagePlayerLookUp(bot))