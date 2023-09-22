import os

from datetime import timedelta
from flask import Blueprint, session, redirect, request, url_for, flash
from requests_oauthlib import OAuth2Session
from flask_login import login_user, logout_user, current_user

from .utilities.constants.constants import *
from . import db
from .models import discordAccount

AUTHORIZATION_BASE_URL = API_BASE_URL + '/oauth2/authorize'
TOKEN_URL = API_BASE_URL + '/oauth2/token'

discordauth = Blueprint('discordauth', __name__)

if 'http://' in OAUTH2_REDIRECT_URI:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


def token_updater(token):
    session['oauth2_token'] = token


def make_session(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=OAUTH2_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=TOKEN_URL,
        token_updater=token_updater)


@discordauth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('bot.root'))
    else:
        scope = request.args.get(
            'scope',
            'identify guilds')
        discord = make_session(scope=scope.split(' '))
        authorization_url, state = discord.authorization_url(
            AUTHORIZATION_BASE_URL)
        session['oauth2_state'] = state
        return redirect(authorization_url)


@discordauth.route('/callback')
def callback():
    if request.values.get('error'):
        flash(request.values['error'], category='error')
        return redirect(url_for('bot.login'))
    discord = make_session(state=session.get('oauth2_state'))
    token = discord.fetch_token(
        TOKEN_URL,
        client_secret=OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session['oauth2_token'] = token

    discord = make_session(token=session.get('oauth2_token'))
    user = discord.get(API_BASE_URL + '/users/@me').json()
    discordUser = discordAccount.query.filter_by(id=user['id']).first()
    if not discordUser:
        new_user = discordAccount(
            id=user['id'],
            username=user['username'],
            accent_color=user['accent_color'],
            avatar=user['avatar'],
            avatar_decoration=user['avatar_decoration'],
            banner=user['banner'],
            banner_color=user['banner_color'],
            discriminator=user['discriminator']
        )
        db.session.add(new_user)
        db.session.commit()
    else:
        discordUser.username = user['username']
        discordUser.accent_color = user['accent_color']
        discordUser.avatar = user['avatar']
        discordUser.avatar_decoration = user['avatar_decoration']
        discordUser.banner = user['banner']
        discordUser.banner_color = user['banner_color']
        discordUser.discriminator = user['discriminator']
        db.session.commit()
    discordUser = discordAccount.query.filter_by(id=user['id']).first()
    login_user(discordUser, remember=True, duration=timedelta(days=7))
    return redirect(url_for('bot.root'))


# @discordauth.route('/me')
# def me():
#     discord = make_session(token=session.get('oauth2_token'))
#     user = discord.get(API_BASE_URL + '/users/@me').json()
#     guilds = discord.get(API_BASE_URL + '/users/@me/guilds').json()
#     return jsonify(user=user, guilds=guilds)

@discordauth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('bot.root'))
