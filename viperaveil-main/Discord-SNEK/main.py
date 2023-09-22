"""
Runs Vipera Veil Bot in Production 'Mode'
"""
import os
import logging
import sys
token = os.environ.get('TOKEN')
import asyncio
from viperasnek import main as viperaveilworker

logging.basicConfig(filename='discord.log',encoding='utf-8',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.stdout = open('discord.log', 'w')

if __name__ == '__main__':
    asyncio.run(viperaveilworker(token))
