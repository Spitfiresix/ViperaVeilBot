import asyncio

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import select
from sqlalchemy import String
from sqlalchemy import MetaData
from sqlalchemy import Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import UUID
import uuid

metadata = MetaData()
Base = declarative_base()


class Partial_Register(Base):
    __tablename__ = 'Partial_Register'

    discordid = Column(String(128), unique=True, primary_key=True)
    discord = Column(String(128), unique=True)
    handle = Column(String(128), unique=True)
    key = Column(String(128), unique=True)
    rsi_id = Column(String(128), unique=True)

    __mapper_args__ = {"eager_defaults": True}


class Playlist(Base):
    __tablename__ = 'playlist'

    user = Column(String(32), primary_key=True)
    name = Column(String(50))
    title = Column(String(512))
    link = Column(String(128))

    __mapper_args__ = {"eager_defaults": True}


class Queue(Base):
    __tablename__ = 'queue'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    server = Column(String(32))
    isPlaying = Column(Boolean())
    requester = Column(String(50))
    textChannel = Column(String(50))
    voiceChannel = Column(String(50))
    track = Column(String(128))
    title = Column(String(512))
    duration = Column(Integer())
    thumb = Column(String(128))
    index = Column(Integer(), nullable=False)

    __mapper_args__ = {"eager_defaults": True}


class Server(Base):
    __tablename__ = 'server'

    server = Column(String(32), primary_key=True)
    prefix = Column(String(10))
    loop = Column(Boolean())
    loopQueue = Column(Boolean())
    shuffle = Column(Boolean())
    djRole = Column(String(50))
    volume = Column(Integer())
    message = Column(String(32))

    __mapper_args__ = {"eager_defaults": True}


class Skip(Base):
    __tablename__ = 'skip'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    server = Column(String(50))
    user = Column(String(50))

    __mapper_args__ = {"eager_defaults": True}

class Matches(Base):
    __tablename__ = 'matches'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    server = Column(String(32))
    isOngoing = Column(Boolean())
    textChannels = Column(String(512))
    voiceChannels = Column(String(512))

    __mapper_args__ = {"eager_defaults": True}

class PlayerRef(Base):
    __tablename__ = 'playerref'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    match = Column(String(32))

    __mapper_args__ = {"eager_defaults": True}

class TempVoice(Base):
    __tablename__ = 'tempvoice'

    id = Column(String(128), primary_key=True)
    server = Column(String(128))

    __mapper_args__ = {"eager_defaults": True}