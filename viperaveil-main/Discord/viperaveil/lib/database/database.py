import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from viperaveil.lib.database.models import Partial_Register
from sqlalchemy import select, update, insert, delete

POSTGRES_URL = 'postgres-viperaveil.postgres.svc.cluster.local:5434'
POSTGRES_USER = 'viperaveil'
POSTGRES_PW = '7xwlf2r08mhz'
POSTGRES_DB = 'viperaveil'
if (os.environ.get('DEBUG_MODE') == 'True'):
    DB_NAME = "database.db"
    DB_URL = f'sqlite:///{DB_NAME}'

else:
    DB_URL = 'postgresql+asyncpg://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)


class DatabaseConnection:
    def __init__(self):
        self.engine = create_async_engine(DB_URL, echo=False)
        self.session = None

    def __enter__(self) -> Session:
        self.session = sessionmaker(bind=self.engine)()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    async def GetSession(self):
        self.engine = create_async_engine(DB_URL, echo=False)
        self.session = sessionmaker(bind=self.engine)()
        return self.session

    async def Partial_Register_select_all(self):
        result = (await self.session.execute(select(Partial_Register))).all()
        return result

    async def Partial_Register_select_specific(self, handle=None, rsi_id=None, discordid=None, key=None):
        data = None
        if handle:
            data = (await self.session.execute(select(Partial_Register).where(Partial_Register.handle == handle))).first()
        elif rsi_id:
            data = (await self.session.execute(select(Partial_Register).where(Partial_Register.rsi_id == rsi_id))).first()
        elif discordid:
            data = (await self.session.execute(select(Partial_Register).where(Partial_Register.discordid == discordid))).first()
        elif key:
            data = (await self.session.execute(select(Partial_Register).where(Partial_Register.key == key))).first()
        if data:
            return data  # [0]
        else:
            return None

    async def Partial_Register_Update(self, rsi_id:str, discordid: str, handle: str, discord: str, key: str):
        await self.session.execute(update(Partial_Register).where(Partial_Register.discord == discord).values(
            rsi_id=rsi_id,
            discordid=discordid,
            handle=handle,
            discord=discord,
            key=key
        ))
        result = (await self.session.execute(select(Partial_Register).where(Partial_Register.discordid == discordid))).all()
        await self.session.commit()
        return result[0]

    async def Partial_Register_insert(self, rsi_id:str, discordid: str, handle: str, discord: str, key: str):
        if self and handle and discord and key:
            await self.session.execute(insert(Partial_Register).values(
                rsi_id=rsi_id,
                discordid=discordid,
                handle=handle,
                discord=discord,
                key=key
            ))
            await self.session.commit()
