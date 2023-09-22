"""
Inter-Bot Communication Cog

Holds all data required for receiving and sending payloads to other bot instances
"""

# import discord
import asyncio
import logging
# from discord import app_commands, ui, Interaction
from discord.ext import commands
logger = logging.getLogger('discord')
import socket
import threading
import sys
host = 'localhost'
port = 8765

class Interconn(commands.Cog):
    """
    Cog description should go here
    """

    def __init__(self, bot):
        self.bot = bot

    class client(threading.Thread):
        def __init__(self, conn):
            super(Interconn.client, self).__init__()
            self.conn = conn
            self.data = ""

        def run(self):
            while True:
                self.data = self.data + str(self.conn.recv(1024))
                if self.data.endswith(u"\r\n"):
                    print(self.data)
                    self.data = ""

        def send_msg(self,msg):
            self.conn.send(msg)

        def close(self):
            self.conn.close()

    class connectionThread(threading.Thread):
        def __init__(self, host, port, bot):
            self.bot = bot
            super(Interconn.connectionThread, self).__init__()
            try:
                self.bot.interconn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s = self.bot.interconn
                self.s.bind((host,port))
                self.s.listen(20)
            except socket.error:
                print('Failed to create socket')
                sys.exit()
            self.clients = []

        def run(self):
            greet = bytes(f'\r\nConnected to {self.bot.user.id}\r\n', 'utf-8')# self.bot.user.name
            while True:
                conn, address = self.s.accept()
                c = Interconn.client(conn)
                c.start()
                c.send_msg(greet)
                self.clients.append(c)
                print ('[+] Client connected: {0}'.format(address[0]))

    @commands.Cog.listener()
    async def on_ready(self):
        get_conns = Interconn.connectionThread(host, port, self.bot)
        get_conns.start()
        while True:
            try:
                response = b'Polling...'
                for c in get_conns.clients:
                    if c.data.endswith("b'\\r\\n'"):
                        if c.data.__contains__('identifier'):
                            print(str(c.data))
                            c.data = ""
                            c.send_msg(response + b"\r\n")
            except:
                pass

def setup(bot):
    """Imports Cog class on class import"""
    bot.add_cog(Interconn(bot))
