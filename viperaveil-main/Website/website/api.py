import os
from flask import Blueprint, request, jsonify, Response, url_for, redirect, render_template
from flask_login import login_required, current_user
from flask_restx import Resource, Api, Namespace
from sqlalchemy import null, or_
from . import api
from . import db
from .models import apiUser, discordUser, rsiUser, rsiOrg, viperaUser, application, Matches, MatchRef
from sqlalchemy.sql import func
from flask_jwt_extended import jwt_required
from .utilities.rsi.lookup import apiRSILookup
from datetime import datetime, timedelta
import json
from .utilities.sqlalchemy.encoders import AlchemyEncoder
from .utilities.external_apis.tiktok import tt_latest_lookup
import logging

logger = logging.getLogger('waitress')
apiBlueprint = Blueprint('api', __name__)
api = Api(apiBlueprint, version='1.0', title='Vipera Veil API',
          description='Facilitating data transfers for Vipera Veil')
# assert url_for('api.doc') == '/api/doc/'

rsiNS = Namespace(
    name='rsi',
    description='For methods relating to RSI accounts')
viperaNS = Namespace(
    name='vipera',
    description='For methods relating to Vipera Veil accounts')
externalNS = Namespace(
    name='external',
    description='Connecting to external services/APIs'
)
eventNS = Namespace(
    name='events',
    description='For methods relating to SNEK WARS'
)


def orgNeedUpdate(sid):
    org = db.session.query(rsiOrg).filter(rsiOrg.sid == sid).first()
    if org:
        now = datetime.now()
        lastUpdate = org.createdDate
        diff = now - lastUpdate
        if diff > timedelta(hours=1):
            return True
        else:
            return False
    else:
        return None


def userNeedUpdate(handle):
    user = db.session.query(rsiUser).filter(rsiUser.handle == handle).first()
    if user:
        now = datetime.now()
        lastUpdate = user.createdDate
        diff = now - lastUpdate
        if diff > timedelta(hours=1):
            return True
        else:
            return False
    else:
        return None


def rsiUserRows(user):
    rsiuserrow = rsiUser(
        id=None,
        handle=user['data']['profile']['handle'],
        badge=user['data']['profile']['badge'],
        badge_image=user['data']['profile']['badge_image'],
        bio=user['data']['profile']['bio'],
        display=user['data']['profile']['display'],
        enlisted=user['data']['profile']['enlisted'],
        fluency=user['data']['profile']['fluency'],
        recordID=user['data']['profile']['id'],
        image=user['data']['profile']['image'],
        website=user['data']['profile']['website'],
        title=user['data']['profile']['page']['title'],
        url=user['data']['profile']['page']['url'],
        rank=user['data']['organization']['rank'],
        stars=user['data']['organization']['stars'],
        org=user['data']['organization']['sid'],
        createdDate=datetime.now())
    return rsiuserrow


def rsiOrgRows(user):
    rsiorgrow = rsiOrg(
        id=None,
        sid=user['data']['organization']['sid'],
        image=user['data']['organization']['image'],
        name=user['data']['organization']['name'],
        url=f"https://robertsspaceindustries.com/orgs/{user['data']['organization']['sid']}",
        members=user['data']['organization']['members'],
        createdDate=datetime.now())
    return rsiorgrow


def rsiOrgSpecRows(org):
    rsiorgrow = rsiOrg(
        id=None,
        sid=org['data']['organization']['sid'],
        image=org['data']['organization']['image'],
        name=org['data']['organization']['name'],
        url=org['data']['organization']['url'],
        members=org['data']['organization']['members'],
        tags=str(org['data']['organization']['tags']),
        createdDate=datetime.now())
    return rsiorgrow


def discordUserRows(user):
    discordUserRow = discordUser(
        id=None,
        discord_id=user['discordData']['discord_id'],
        display_name=user['discordData']['display_name'],
        name=user['discordData']['name'],
        nick=user['discordData']['nick'],
        joined_at=datetime.strptime(
            user['discordData']['joined_at'],
            '%Y-%m-%d %H:%M:%S.%f%z'),
        createdDate=datetime.now())
    return discordUserRow


def viperaUserRows(user):
    viperaUserRow = viperaUser(
        id=None,
        discorduser_id=user['DiscordUserID'],
        discorduser_handle=user['DiscordHandle'],
        rsiuser_id=user['RSIUserID'],
        rsiuser_handle=user['RSIHandle'],
        createdDate=datetime.now()
    )
    return viperaUserRow


def applicationRows(application):
    applicationRows = application(
        appid=application['appid'],
        applicationdate=application['applicationdate'],
        discordname=application['discordname'],
        rsiname=application['rsiname'],
        region=application['region'],
        interest=application['interest'],
        scstartdate=application['scstartdate'],
        expectations=application['expectations'],
        role=application['role'],
        ships=application['ships'],
        refer=application['refer'],
        competitive=application['competitive'],
        pastorgs=application['pastorgs'],
        controls=application['controls'],
        realworldskills=application['realworldskills'],
        strengthsandweakness=application['strengthsandweakness'],
        email=application['email'],
        recruiter=application['recruiter'],
        status=application['status']
    )
    return applicationRows


# @api.route('/', endpoint='ViperaVeil', doc=False)
# class index(Resource):
#     def get(self):
#         #return 'Welcome to the Vipera Veil API'
#         return redirect('/api/doc/')

# @api.route('/api/rsi')
# class index

##########   NAMESPACE EVENTS  #########

## RSI Namespace ##

@rsiNS.route('/user')
@rsiNS.doc(security='apikey')
class rsiuserList(Resource):
    @jwt_required(fresh=True)
    def get(self):
        user = db.session.query(rsiUser).all()
        if user:
            return user, 201
        else:
            return 'User table empty', 201


@rsiNS.route('/user/<id>')
@rsiNS.doc(security='apikey')
class rsiuserSearch(Resource):
    @jwt_required(fresh=True)
    def get(self, id):
        user = db.session.query(rsiUser).filter(
            func.lower(rsiUser.handle) == func.lower(id)).first()
        maindict = {}
        maindict['data'] = {}
        orgPresent = False
        if not user:
            # User doesn't exist in db
            user = apiRSILookup(inputData=id, apiLoc='user')
            if user == 'Player does not exist':
                # player doesn't exist, returning
                return user, 404
            # Found user, creating in db and returning
            # Create Data in db
            rsiUserRow = rsiUserRows(user)
            db.session.add(rsiUserRow)
            if user['data']['organization'].get('sid'):
                orgPresent = True
                orgSID = user['data']['organization'].get('sid')
                if orgNeedUpdate(orgSID):
                    rsiOrgRow = db.session.query(rsiOrg).where(
                        rsiOrg.sid == user['data']['organization']['sid']).first()
                    rsiOrgRow.image = user['data']['organization']['image']
                    rsiOrgRow.name = user['data']['organization']['name']
                    rsiOrgRow.url = f"https://robertsspaceindustries.com/orgs/{user['data']['organization']['sid']}"
                    rsiOrgRow.members = user['data']['organization']['members']
                    rsiOrgRow.createdDate = datetime.now()
                elif orgNeedUpdate(orgSID) is None:
                    rsiOrgRow = rsiOrgRows(user)
                    db.session.add(rsiOrgRow)
            db.session.commit()
            user = db.session.query(rsiUser).filter(func.lower(
                rsiUser.handle) == func.lower(id)).first()
            if hasattr(user, 'org'):
                orgPresent = True
                if not db.session.query(rsiOrg).filter(
                        rsiOrg.sid == user.org).first():
                    userdata = apiRSILookup(user.handle.lower(), 'user')
                    rsiOrgRow = rsiOrgRows(userdata)
                    db.session.add(rsiOrgRow)
                    db.session.commit()
            userjson = json.dumps(user, cls=AlchemyEncoder)
            userdict = json.loads(userjson)
            userdict['enlisted'] = str(user.enlisted)
            userdict.pop('query')
            userdict.pop('query_class')
            userdict.pop('registry')
            userdict.pop('serialize')
            userdict.pop('createdDate')
            if orgPresent:
                org = db.session.query(rsiOrg).filter(
                    rsiOrg.sid == user.org).first()
                orgjson = json.dumps(org, cls=AlchemyEncoder)
                orgDict = json.loads(orgjson)
                orgDict.pop('query')
                orgDict.pop('query_class')
                orgDict.pop('registry')
                orgDict.pop('serialize')
                orgDict.pop('createdDate')
                maindict['data']['organization'] = orgDict
            maindict['data']['profile'] = userdict
            maindict['source'] = 'live'
            return maindict, 201
        elif userNeedUpdate(handle=user.handle):
            user = apiRSILookup(inputData=id, apiLoc='user')
            user['data']['profile']['enlisted'] = str(
                user['data']['profile']['enlisted'])
            if user == 'Player does not exist':
                return user, 201
            if user['data']['organization'].get('sid'):
                orgPresent = True
                if orgNeedUpdate(user['data']['organization']['sid']):
                    # Update org table
                    rsiOrgRow = db.session.query(rsiOrg).where(
                        rsiOrg.sid == user['data']['organization']['sid']).first()
                    rsiOrgRow.image = user['data']['organization']['image']
                    rsiOrgRow.name = user['data']['organization']['name']
                    rsiOrgRow.url = f"https://robertsspaceindustries.com/orgs/{user['data']['organization']['sid']}"
                    rsiOrgRow.members = user['data']['organization']['members']
                    rsiOrgRow.createdDate = datetime.now()
            # Update user Data in db
            rsiUserRow = db.session.query(rsiUser).where(
                rsiUser.handle == user['data']['profile']['handle']).first()
            rsiUserRow.badge = user['data']['profile']['badge']
            rsiUserRow.bio = user['data']['profile']['bio']
            rsiUserRow.display = user['data']['profile']['display']
            rsiUserRow.enlisted = datetime.strptime(
                user['data']['profile']['enlisted'], "%Y-%m-%d %H:%M:%S")
            rsiUserRow.fluency = user['data']['profile']['fluency']
            rsiUserRow.recordID = user['data']['profile']['id']
            rsiUserRow.image = user['data']['profile']['image']
            rsiUserRow.website = user['data']['profile']['website']
            rsiUserRow.title = user['data']['profile']['page']['title']
            rsiUserRow.url = user['data']['profile']['page']['url']
            rsiUserRow.rank = user['data']['organization']['rank']
            rsiUserRow.stars = user['data']['organization']['stars']
            rsiUserRow.org = user['data']['organization']['sid']
            rsiUserRow.createdDate = datetime.now()
            db.session.commit()
            user = db.session.query(rsiUser).filter(
                func.lower(rsiUser.handle) == func.lower(id)).first()
            userjson = json.dumps(user, cls=AlchemyEncoder)
            userdict = json.loads(userjson)
            userdict['enlisted'] = str(user.enlisted)
            userdict.pop('query')
            userdict.pop('query_class')
            userdict.pop('registry')
            userdict.pop('serialize')
            userdict.pop('createdDate')
            if orgPresent:
                org = db.session.query(rsiOrg).filter(
                    rsiOrg.sid == user.org).first()
                orgjson = json.dumps(org, cls=AlchemyEncoder)
                orgDict = json.loads(orgjson)
                orgDict.pop('query')
                orgDict.pop('query_class')
                orgDict.pop('registry')
                orgDict.pop('serialize')
                orgDict.pop('createdDate')
                maindict['data']['organization'] = orgDict
            maindict['data']['profile'] = userdict
            maindict['source'] = 'live'
            return maindict, 201
        else:
            if user.org:
                orgPresent = True
                if not db.session.query(rsiOrg).filter(
                        rsiOrg.sid == user.org).first():
                    userdata = apiRSILookup(user.handle.lower(), 'user')
                    rsiOrgRow = rsiOrgRows(userdata)
                    db.session.add(rsiOrgRow)
                    db.session.commit()
            userjson = json.dumps(user, cls=AlchemyEncoder)
            userdict = json.loads(userjson)
            userdict['enlisted'] = str(user.enlisted)
            userdict.pop('query')
            userdict.pop('query_class')
            userdict.pop('registry')
            userdict.pop('serialize')
            userdict.pop('createdDate')
            if orgPresent:
                org = db.session.query(rsiOrg).filter(
                    rsiOrg.sid == user.org).first()
                orgjson = json.dumps(org, cls=AlchemyEncoder)
                orgDict = json.loads(orgjson)
                orgDict.pop('query')
                orgDict.pop('query_class')
                orgDict.pop('registry')
                orgDict.pop('serialize')
                orgDict.pop('createdDate')
                maindict['data']['organization'] = orgDict
            maindict['data']['profile'] = userdict
            maindict['source'] = 'cache'
            return maindict, 201


@rsiNS.route('/org/<id>')
@rsiNS.doc(security='apikey')
class rsiOrgSearch(Resource):
    @jwt_required(fresh=True)
    def get(self, id):
        org = db.session.query(rsiOrg).filter(
            func.lower(rsiOrg.sid) == func.lower(id)).first()
        if not org:
            # User doesn't exist in db
            org = apiRSILookup(inputData=id.lower(), apiLoc='org')
            if org == 'Player does not exist':
                # player doesn't exist, returning
                return org, 404
            rsiOrgRow = rsiOrgSpecRows(org)
            db.session.add(rsiOrgRow)
            db.session.commit()
            org['source'] = 'live'
            return org, 201
        elif orgNeedUpdate(org.sid):
            org = apiRSILookup(inputData=id.lower(), apiLoc='org')
            rsiOrgRow = db.session.query(rsiOrg).where(
                rsiOrg.sid == org['data']['organization']['sid']).first()
            rsiOrgRow.image = org['data']['organization']['image']
            rsiOrgRow.name = org['data']['organization']['name']
            rsiOrgRow.url = org['data']['organization']['url']
            rsiOrgRow.members = org['data']['organization']['members']
            rsiOrgRow.tags = org['data']['organization']['tags']
            rsiOrgRow.createdDate = datetime.now()
            db.session.commit()
            org['source'] = 'live'
            return org, 201
        else:
            orgjson = json.dumps(org, cls=AlchemyEncoder)
            orgDict = json.loads(orgjson)
            orgDict.pop('query')
            orgDict.pop('query_class')
            orgDict.pop('registry')
            orgDict.pop('serialize')
            orgDict.pop('createdDate')
            maindict = {}
            maindict['data'] = {}
            maindict['data']['organization'] = orgDict
            maindict['source'] = 'cache'
            return maindict, 201

## Vipera Namespace ##

@viperaNS.route('/link/<id>')
@viperaNS.doc(security='apikey')
class rsiLink(Resource):
    @jwt_required(fresh=True)
    def get(self, id):
        user = apiRSILookup(inputData=id.lower(), apiLoc='user')
        if not user == 'Player does not exist':
            data = {
                'handle': user['data']['profile']['handle'],
                'bio': user['data']['profile']['bio'],
                'org': user['data']['organization']['sid'] if user['data'].get('organization').get('sid') else None
            }
            return data, 201
        else:
            return user, 404

@viperaNS.route('/user/<id>')
@viperaNS.doc(security='apikey')
class viperausersearch(Resource):
    @jwt_required(fresh=True)
    def get(self, id):
        vipera = db.session.query(viperaUser).filter(
            viperaUser.id == id).first()
        if vipera:
            return vipera, 201
        else:
            return vipera, 404


@viperaNS.route('/user')
@viperaNS.doc(security='apikey',
              params={'DiscordUserID': 'UserID for Discord account to create/update',
                      'DiscordHandle': 'Discord Handle for Discord account to create/update',
                      'RSIHandle': 'RSI Handle to link to Discord account',
                      'RSIUserID': 'RSI ID associated with handle',
                      'discordData': 'A dict for multiple parts of an account'})
class viperauser(Resource):
    @jwt_required(fresh=True)
    def put(self):
        if request.json or request.args:
            if request.json:
                data = request.json
            else:
                data = request.args
        else:
            return 'Invalid Data', 404
        if not data['DiscordUserID']:
            return 'Missing DiscordUserID', 404
        if not data['DiscordHandle']:
            return 'Missing DiscordHandle', 404
        if not data['RSIUserID']:
            return 'Missing RSIUserID', 404
        if not data['RSIHandle']:
            return 'Missing RSIHandle', 404
        discord = db.session.query(discordUser).filter(
            discordUser.discord_id == data['DiscordUserID']).first()
        if discord:
            discord.discord_id = data['discordData']['discord_id']
            discord.display_name = data['discordData']['display_name']
            discord.name = data['discordData']['name']
            discord.nick = data['discordData']['nick']
            discord.joined_at = data['discordData']['joined_at']
            createdDate = datetime.now()
            db.session.commit()
        else:
            discordUserRow = discordUserRows(data)
            db.session.add(discordUserRow)
            db.session.commit()
        vipera = db.session.query(viperaUser).filter(
            or_(
                viperaUser.discorduser_id == data['DiscordUserID'],
                viperaUser.rsiuser_handle == data['RSIHandle'])).first()
        if vipera:
            vipera.discorduser_id = data['DiscordUserID']
            vipera.discorduser_handle = data['DiscordHandle']
            vipera.rsiuser_handle = data['RSIHandle']
            vipera.rsiuser_id = data['RSIUserID']
            db.session.commit()
            return 'User already exists, updating', 201
        else:
            viperaUserRow = viperaUserRows(data)
            db.session.add(viperaUserRow)

            db.session.commit()
            return 'New user created', 201


@viperaNS.route('/application')
class submitapplication(Resource):
    @jwt_required(fresh=True)
    def post(self):
        incomingData = request.json
        appid = incomingData['appid']
        applicant = db.session.query(application).filter(or_(
            application.appid == appid, application.discordname == incomingData['discordname'])).first()
        if applicant:
            db.session.commit()
            return appid, 201
        else:
            incomingData.status = 'pending'
            applicationRow = applicationRows(incomingData)
            db.session.add(applicationRow)
            db.session.commit()
            return appid, 201


@viperaNS.route('/application/<appid>')
@viperaNS.doc(security='apikey')
class viperaapplicationsearchbyid(Resource):
    @jwt_required(fresh=True)
    def get(self, appid):
        vipera = db.session.query(application).filter(
            application.appid == appid).first()
        if vipera:
            return vipera, 201
        else:
            return vipera, 404


@viperaNS.route('/application/<discordname>')
@viperaNS.doc(security='apikey')
class viperaapplicationsearchbyname(Resource):
    @jwt_required(fresh=True)
    def get(self, discordname):
        vipera = db.session.query(application).filter(
            application.discordname == discordname).first()
        if vipera:
            return vipera, 201
        else:
            return vipera, 404


@viperaNS.route('/application/<status>')
@viperaNS.doc(security='apikey')
class viperaapplicationsearchbyid(Resource):
    @jwt_required(fresh=True)
    def get(self, status):
        vipera = db.session.query(application).filter(
            application.status == status).all()
        if vipera:
            return vipera, 201
        else:
            return vipera, 404


@viperaNS.route('/application/')
@viperaNS.doc(security='apikey')
class applicationList(Resource):
    @jwt_required(fresh=True)
    def get(self):
        app = db.session.query(application).all()
        if app:
            return app, 201
        else:
            return 'app table empty', 201

## External Services Namespace ##

@externalNS.route('/tiktok/<id>')
@externalNS.doc(security='apikey',
                params={'id': 'TikTok user id to lookup'})
class TTLookup(Resource):
    @jwt_required(fresh=True)
    def get(self, id):
        data = tt_latest_lookup(id)
        return data


## Event Namespace ##

@eventNS.route('/matches/')
@eventNS.doc(security='apikey')
class Matches(Resource):
    @jwt_required(fresh=True)
    def get(self):
        matches = db.session.query(Matches).all()
        if matches:
            return matches, 201
        else:
            return 'Matches table empty', 201

@eventNS.route('/matches/')
@eventNS.param(name='id', description='Match ID')
@eventNS.param(name='date', description='Date that Match took place')
@eventNS.doc(security='apikey')
class MatchesSearch(Resource):
    @jwt_required(fresh=True)
    def get(self):
        incomingData = request.json
        return incomingData