"""
Vipera Bot API Cog
"""

import asyncio
import discord
import logging
import os
import asyncio
import threading
import functools
import json
import queue
from aiohttp import web
from discord import ui, Interaction
from flask import Flask, Blueprint, request, jsonify, Response, url_for, redirect, render_template
from flask_login import login_required, current_user
from flask_restx import Resource, Api, Namespace
from discord.ext import commands, tasks
from waitress import serve
from viperaveil.utilities.Constants import discord_roles, developer_role
logger = logging.getLogger('discord')

app = Flask(__name__)
api = Api(app)

def build_namespace(name, description, bot):
    ns = Namespace(
        name = name,
        description = description,
        bot=bot
    )
    return ns

class DiscordEvent(Resource):
    def __init__(self, api, bot):
        self.bot = bot

    def get(self):
        return self.bot.user.id, 200
        #return {'message': 'Success!'}, 200

class ViperaAPI(commands.Cog):
    """
    Bot external events Cog
    """

    def __init__(self, bot):
        self.bot = bot
        self.app = app
        self.api = api

        self.event_queue = queue.Queue()

        async def event_listener():
            testing_guild: discord.Guild = bot.get_guild(303245408539246603)
            #testing_channel: discord.TextChannel = testing_guild.get_channel(643072384001114112)
            #await testing_channel.send(content='Sent via Vipera API', delete_after=20)
            return testing_guild.name
        
        async def team_role_export():
            role_export = []
            users_added = []
            vipera_guild: discord.Guild = bot.get_guild(303245408539246603)
            for role in discord_roles:
                current_role: discord.Role = vipera_guild.get_role(role[0])
                current_roles_members = current_role.members
                for member in current_roles_members:
                    member: discord.Member = member
                    if not member.id in users_added:
                        users_added.append(member.id)
                        data = (member.id, member.display_name, member.display_avatar.url, current_role.name)
                        role_export.append(data)
            return role_export
        
        async def devs_role_export():
            role_export = []
            users_added = []
            vipera_guild: discord.Guild = bot.get_guild(303245408539246603)
            for role in developer_role:
                current_role: discord.Role = vipera_guild.get_role(role[0])
                current_roles_members = current_role.members
                for member in current_roles_members:
                    member: discord.Member = member
                    if not member.id in users_added:
                        users_added.append(member.id)
                        data = (member.id, member.display_name, member.display_avatar.url, current_role.name)
                        role_export.append(data)
            return role_export

        self.api.add_resource(DiscordEvent, '/discord-event', resource_class_kwargs={'bot': bot})

        self.musicNS = Namespace('music', 'For methods relating to Music Control')
        self.discordNS = Namespace('discord', 'Exporting Discord user/server info')
        #musicNS.add_resource(MusicControl, resource_class_kwargs={'bot': bot})

        @self.musicNS.route('/control')
        @self.musicNS.doc(params={'guild': 'Guild ID to run the command against', 'command': 'Command to send to the Bot/API'})
        class MusicControl(Resource):
            def get(self):
                if request.json:
                    guild = int(request.json['guild'])
                    command = request.json['command']
                else:
                    guild = int(request.args['guild'])
                    command = request.args['command']
                return redirect(url_for('.async_music_control', guild=guild, command=command), code=307)
        
        @self.discordNS.route('/staff')
        class DiscordStaff(Resource):
            def get(self):
                return redirect(url_for('.async_discord_staff'), code=307)
            
        @self.discordNS.route('/devs')
        class DiscordStaff(Resource):
            def get(self):
                return redirect(url_for('.async_discord_devs'), code=307)
            
        @self.discordNS.route('/webhook')
        @self.discordNS.doc(params={'endpoint':'Endpoint to send payload to', 'payload': 'Payload to pass with endpoint as body formatted in XML'})
        class webhook(Resource):
            def post(self):
                endpoint = request.args['endpoint']
                payload = request.data
                bot.event_loop_list.append((endpoint, payload.decode()))
                return 'Success',202


        @self.app.route('/async/music/control', methods=['GET'])
        async def async_music_control():
            guild = int(request.args['guild'])
            command = request.args['command']
            guild_name = await event_listener()
            print(f'Bot ID - {bot.user.id}')
            return f'{guild}-{command}-{guild_name}', 200
        
        @self.app.route('/async/discord/yt_webhook', methods=['POST'])
        async def async_discord_yt_webhook():
            endpoint = 'yt_webhook'
            payload = request.data
            bot.event_loop_list.append((endpoint, payload))
            return 'Success', 202
        
        @self.app.route('/async/discord/staff', methods=['GET'])
        async def async_discord_staff():
            role_export = await team_role_export()
            return jsonify(role_export), 200
        
        @self.app.route('/async/discord/devs', methods=['GET'])
        async def async_discord_devs():
            role_export = await devs_role_export()
            return jsonify(role_export), 200

        self.api.add_namespace(self.musicNS)
        self.api.add_namespace(self.discordNS)

    def start_flask_app(self):
        #self.app.run(debug=False, host='0.0.0.0', use_reloader=False)
        serve(self.app, listen="0.0.0.0:5000",connection_limit=1000,url_scheme='http',threads=1000)

    def stop_flask_app(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    # @tasks.loop()
    # async def web_server(self):
    #     runner = web.AppRunner(self.app)
    #     await runner.setup()
    #     site = web.TCPSite(runner, host='127.0.0.1', port=5000)
    #     await site.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__class__.__name__} cog is ready')
        #ViperaAPI.web_server(self).start()
        #self.start_flask_app()
        self.flask_thread = threading.Thread(target=self.start_flask_app)
        self.flask_thread.daemon = True
        self.flask_thread.start()

    @commands.Cog.listener()
    async def on_cog_unload(self):
        print(f'{self.__class__.__name__} cog is unloaded')
        self.stop_flask_app()

def setup(bot):
    """Imports Cog class on class import"""
    bot.add_cog(ViperaAPI(bot))
