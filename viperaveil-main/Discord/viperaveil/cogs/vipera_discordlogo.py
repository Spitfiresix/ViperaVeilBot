import asyncio
import logging
import os
import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO

logger = logging.getLogger('discord')

class ViperaDiscordLogo(commands.Cog):
    """
    Layer discord logo on top of Icon 
    """
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')
    
    @commands.guild_only()
    @discord.slash_command(name='makepfp',
                          description='paste your image and create a pfp')
    async def makepfp(self,ctx: discord.ApplicationContext, pfp: discord.Attachment):
        #make PFP
        # URL of the images you want to download
        await ctx.defer()
        sneklogo = "./assets/SNEKTRNSPRNT-01.png"
        file_name = f"./viperaveil/cache/{ctx.user.id}.png"

        # Check if the requests were successful
        # Open the images from the response content
        image: Image.Image = Image.open(BytesIO(await pfp.read())).convert("RGBA")
        image2: Image.Image = Image.open(sneklogo).convert("RGBA")

        # Resize the second image to match the size of the first image
        image = image.resize(image2.size, resample=Image.LANCZOS)

        # Create a new blank image with alpha channel
        composite_image = Image.new("RGBA", image2.size)

        # Composite the images
        composite_image = Image.alpha_composite(composite_image, image)
        composite_image = Image.alpha_composite(composite_image, image2)

        # Show the composite image
        composite_image.save(file_name)
        f = open(file_name, 'rb')
        file = discord.File(f, f"{ctx.user.id}.png")
        await ctx.followup.send(file=file, delete_after=40)
        file.close()
        f.close()
        os.remove(file_name)


def setup(bot):
    """Imports Cog class on module import"""
    bot.add_cog(ViperaDiscordLogo(bot))
