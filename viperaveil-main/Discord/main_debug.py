"""
Runs Vipera Veil Bot in Development 'Mode'
"""
import os
os.environ.setdefault('DEBUG_MODE', 'True')
import asyncio
import logging
import sys
from viperaveil import main as viperaveilconnector

logging.basicConfig(filename='discord.log',encoding='utf-8',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.stdout = open('discord.log', 'w')


if __name__ == '__main__':
    asyncio.run(viperaveilconnector(), debug=True)
