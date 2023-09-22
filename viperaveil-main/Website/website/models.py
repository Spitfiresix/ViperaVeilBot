from sqlalchemy.dialects import postgresql
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, Integer, String, inspect, event
import datetime

# Migration steps when changing table columns/schema
# 1. $env:FLASK_APP = 'mainDebug.py'
# 2. flask db stamp head
# 3. flask db migrate -m "change notes"
# 4. flask db upgrade

####### Vipera Veil API Models #######


class apiUser(db.Model):
    __tablename__ = 'api_user'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    displayName = db.Column(db.String(128), unique=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    createdDate = db.Column(db.DateTime(timezone=False), default=func.now())

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def insert_starting_data():
        row = apiUser(
            displayName='DiscordBot',
            username='Discord',
            password='adminforbot',
            email='discord@hotmail.com',
            createdDate=datetime.datetime.now()
        )
        db.session.add(row)
        db.session.commit()


class discordUser(db.Model):
    __tablename__ = 'discord_user'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    discord_id = db.Column(db.String(36), primary_key=True)
    display_name = db.Column(db.String(64))
    name = db.Column(db.String(64))
    nick = db.Column(db.String(64))
    joined_at = db.Column(db.DateTime(timezone=False), default=func.now())
    createdDate = db.Column(db.DateTime(timezone=False), default=func.now())

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class rsiUser(db.Model):
    __tablename__ = 'rsi_user'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    handle = db.Column(db.String(64), unique=True)
    badge = db.Column(db.String(128))
    badge_image = db.Column(db.String(512))
    bio = db.Column(db.String(1024), default=None)
    display = db.Column(db.String(32))
    enlisted = db.Column(db.DateTime(timezone=False))
    fluency = db.Column(db.String(64))
    recordID = db.Column(db.String(32))
    image = db.Column(db.String(512))
    website = db.Column(db.String(128), default=None)
    title = db.Column(db.String(64))
    url = db.Column(db.String(128))
    rank = db.Column(db.String(64))
    stars = db.Column(db.String(12))
    org = db.Column(db.String(12))
    createdDate = db.Column(db.DateTime(timezone=False), default=func.now())

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class rsiOrg(db.Model):
    __tablename__ = 'rsi_org'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    sid = db.Column(db.String(32), unique=True)
    image = db.Column(db.String(512))
    name = db.Column(db.String(128))
    url = db.Column(db.String(128))
    tags = db.Column(db.String(128))
    members = db.Column(db.String(32))
    createdDate = db.Column(db.DateTime(timezone=False), default=func.now())

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class viperaUser(db.Model):
    __tablename__ = 'vipera_user'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    discorduser_id = db.Column(db.String(36), unique=True, nullable=False)
    discorduser_handle = db.Column(db.String(36), nullable=False)
    rsiuser_id = db.Column(db.String(36), unique=True, nullable=False)
    rsiuser_handle = db.Column(db.String(36), unique=True)
    createdDate = db.Column(db.DateTime(timezone=False), default=func.now())

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class events(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(42), nullable=False)
    occurrence = db.Column(db.DateTime(timezone=True))
    repeat = db.Column(db.Boolean, unique=False)
    repeatOccurrence = db.Column(db.String(64), unique=False)
    isFinished = db.Column(db.Boolean, unique=False)

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class application(db.Model):
    __tablename__ = 'application'

    appid = db.Column(db.String(42), primary_key=True)
    applicationdate = db.Column(db.DateTime(timezone=True), )
    discordname = db.Column(db.String(42), unique=True)
    rsiname = db.Column(db.String(42), unique=True)
    region = db.Column(db.String(42), unique=False)
    interest = db.Column(db.String(42), unique=False)
    scstartdate = db.Column(db.String(42), unique=False)
    expectations = db.Column(db.String(42), unique=False)
    role = db.Column(db.String(42), unique=False)
    ships = db.Column(db.String(42), unique=False)
    refer = db.Column(db.String(42), unique=False)
    competitive = db.Column(db.String(42), unique=False)
    pastorgs = db.Column(db.String(42), unique=False)
    controls = db.Column(db.String(42), unique=False)
    realworldskills = db.Column(db.String(42), unique=False)
    strengthsandweakness = db.Column(db.String(42), unique=False)
    email = db.Column(db.String(42), unique=True)
    recruiter = db.Column(db.String(42), unique=False)
    status = db.Column(db.String(42), unique=False)

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
    
class Matches(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    type = db.Column(db.String(12), unique=False)
    occurrence = db.Column(db.DateTime(timezone=False), default=func.now())
    server = db.Column(db.String(42), unique=False)
    ranked = db.Column(db.Boolean, unique=False)
    victor = db.Column(db.String(42), unique=False)

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

class MatchRef(db.Model):
    __tablename__ = 'matchref'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    team = db.Column(db.String(42), unique=False)
    playerid = db.Column(db.String(42), unique=False)
    matchid = db.Column(db.BigInteger, unique=False)

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

####### Vipera Veil Bot Models #######


class Queue(db.Model):
    __bind_key__ = 'db2'
    __tablename__ = 'queue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server = db.Column(db.String(32))
    isPlaying = db.Column(db.Boolean)
    requester = db.Column(db.String(50))
    textChannel = db.Column(db.String(50))
    track = db.Column(db.String(128))
    title = db.Column(db.String(512))
    duration = db.Column(db.Integer)
    thumb = db.Column(db.String(128))
    index = db.Column(db.Integer, nullable=False)


####### Vipera Veil Website Models #######


class discordAccount(db.Model, UserMixin):
    __tablename__ = 'discord_account'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    accent_color = db.Column(db.Integer)
    avatar = db.Column(db.String(64))
    avatar_decoration = db.Column(db.String(64))
    banner = db.Column(db.String(64))
    banner_color = db.Column(db.String(8))
    discriminator = db.Column(db.String(8))

    def serialize(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
