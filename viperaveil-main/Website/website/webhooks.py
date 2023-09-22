import os
import logging
import json

from datetime import timedelta
from flask import Blueprint, session, redirect, request, url_for, flash, make_response
from flask_restx import Resource, Api, Namespace
from requests_oauthlib import OAuth2Session
from flask_login import login_user, logout_user, current_user
from website.utilities.constants.constants import YT_API_TOPICS
from website.utilities.bot.functions import post_discord_event
import xml.etree.ElementTree as ET

webhooks = Blueprint('webhooks', __name__)

webhooksNS = Namespace(
    name='webhooks',
    description='For methods relating to external webhooks')

@webhooksNS.route('/tiktok')
class tt_index(Resource):
    def get(self):
        return 'Response',200
    def post(self):
        return 'Response',200

@webhooksNS.route('/tiktok/callback')
class tt_callback(Resource):
    def get(self):
        return 'Response',200
    def post(self):
        return 'Response',200

@webhooksNS.route('/youtube')
class yt_index(Resource):
    def get(self):
        content = request.get_data(as_text=True)
        signature = request.headers.get('X-Hub-Signature')
        topic = request.args.get('hub.topic')
        mode = request.args.get('hub.mode')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe':
            response = make_response(challenge)
            response.headers['hub.topic'] = topic
            response.headers['hub.mode'] = mode
            response.headers['hub.challenge'] = challenge
            response.status_code = 200
            return response
        else:
            return 'Payload Invalid', 401
    def post(self):
        payload = request.data
        root = ET.fromstring(payload.decode())
        topic = root.find('.//{http://www.w3.org/2005/Atom}link[@rel="self"]').attrib['href']
        if topic:
            if topic.replace('https://www.youtube.com/xml/feeds/videos.xml?channel_id=','') in YT_API_TOPICS:
                post_discord_event(endpoint='yt_webhook', payload=root)
            else:
                return 'Topic Invalid', 404
        else:
            return 'Payload Invalid', 403

@webhooksNS.route('/youtube/callback')
class yt_callback(Resource):
    def post(self):
        return 'Response',204
