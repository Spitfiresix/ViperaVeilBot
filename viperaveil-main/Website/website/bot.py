import json

from flask_restx import Resource
from flask import Blueprint, request, jsonify, Response
from flask import render_template, make_response, redirect, url_for
from flask_login import login_required, current_user
from .models import Queue
from sqlalchemy import asc

from .utilities.sqlalchemy.encoders import AlchemyEncoder
from .utilities.queue.functions import getImage, setText
from .utilities.bot.functions import get_discord_staff, get_discord_devs

from . import db

bot = Blueprint('bot', __name__)

# @views.route('/bot')
# class bot(Resource):
#     def get(self):
#         # if not request.url_root == 'https://viperaveil.redshiftent.com/':
#         #     return 'Page not found',404
#         return 'Vipera Veil Bot',200

class Object(object):
    pass

@bot.route('/')
def root():
    return render_template('/bot/home.html', user=current_user)


@bot.route('/login')
def login():
    return render_template('/bot/login.html', user=current_user)


@bot.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template("/bot/profile.html", user=current_user)
    else:
        return redirect(url_for('discordAuth.login'))

@bot.route('/info')
def pipelines():
    return render_template('/bot/info.html', user=current_user)

@bot.route('/bot/join-us')
def joinus():
    return 'Bot info'

@bot.route('/team')
def team():
    devs_export = get_discord_devs()
    staff_export = get_discord_staff()
    dev_list = []
    staff_list = []
    for dev in devs_export:
        user = Object()
        user.id = dev[0]
        if '[SNEK]' in dev[1]:
            user.name = dev[1][7:]
        else:
            user.name = dev[1]
        user.avatar = dev[2]
        user.role = dev[3]
        dev_list.append(user)
    for staff in staff_export:
        user = Object()
        user.id = staff[0]
        if '[SNEK]' in staff[1]:
            user.name = staff[1][7:]
        else:
            user.name = staff[1]
        user.avatar = staff[2]
        user.role = staff[3]
        staff_list.append(user)
    return render_template("/bot/team.html", user=current_user, staff_list=staff_list, dev_list=dev_list)

@bot.route('/about')
def about():
    return render_template("/bot/about.html", user=current_user)

@bot.route('/donate')
def donate():
    return render_template("/bot/donate.html", user=current_user)

@bot.route('/privacy')
def privacy():
    return render_template("/bot/privacy.html", user=current_user)

@bot.route('/terms')
def terms():
    return render_template("/bot/terms.html", user=current_user)

@bot.route('/bot/queue')
# @bot.doc(params={'guildid': 'Guild to load queue for'})
def queue():
    # if not request.url_root == 'https://viperaveil.redshiftent.com/':
    #     return 'Page not found',404
    try:
        id = request.args['guildid']
    except:
        id = '0'
    try:
        queuedSongs = db.session.query(Queue).filter(
            Queue.server == id).order_by(asc(Queue.index)).all()
        queueJson = json.dumps(queuedSongs, cls=AlchemyEncoder)
        queueList = json.loads(queueJson)
        totalItems = len(queueList) - 1
        if totalItems < 0:
            totalItems = 0
        if queueList[0]['index'] == -1:
            formerSong = [queueList[0]]
            formerSong[0]['thumb'] = getImage(formerSong[0]['thumb'])
            formerSong[0]['title'] = setText(formerSong[0]['title'])
            del queueList[0]
        if queueList[0]['index'] == 0:
            currentSong = [queueList[0]]
            currentSong[0]['thumb'] = getImage(currentSong[0]['thumb'])
            currentSong[0]['title'] = setText(currentSong[0]['title'])
            del queueList[0]
    except Exception as error:
        print(error)
        queueList = []
    if 'formerSong' not in locals():
        formerSong = []
    if 'currentSong' not in locals():
        currentSong = []
    ascInt = 1
    for item in queueList:
        item['index'] = ascInt
        item['thumb'] = getImage(item['thumb'])
        item['title'] = setText(item['title'])
        ascInt += 1
    headers = {'Content-Type': 'text/html'}
    return make_response(
        render_template(
            '/bot/queue.html',
            user=current_user,
            queueList=queueList,
            totalItems=totalItems,
            formerSong=formerSong,
            currentSong=currentSong),
        200,
        headers)
