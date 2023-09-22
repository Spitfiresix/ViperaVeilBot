"""
Runs Vipera Veil Bot in Development 'Mode'
"""
import os
import logging
import sys
os.environ.setdefault('DEBUG_MODE', 'True')
from multiprocessing import Process
from viperasnek import main as viperaveilworker  # pylint: disable=wrong-import-position
import asyncio  # pylint: disable=wrong-import-position,wrong-import-order

tokens = ['MTEwMjc1Njk2MDg1Nzc1MTU3Mg.G0Lzhm.LZtEztsO81zzRMDdP1GEhlU_jAnnRJzEOmWfjY']#,'MTA2Njg3OTUxMDI2MTI3NjcwMg.G5taV_.mlczVbMshLY1EPGxPckd7kqyjcGWONRkQLEEyY']
#oldtoken = ['MTA2Njg3ODk3OTQxMzM5MzQwOA.GYOaTU.AnUnpmknU43eNDnODHssSFG_9hSRiN89uE3lcA']

process_list = []

logging.basicConfig(filename='discord.log',encoding='utf-8',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sys.stdout = open('discord.log', 'w')

async def base_func(tokens):
    for token in tokens:
        process_list.append(asyncio.create_task(viperaveilworker(token)))
    await asyncio.gather(*process_list)

if __name__ == '__main__':
        #asyncio.run(viperaveilworker(token), debug=True)
        asyncio.run(base_func(tokens))
