# import logging
import os

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from sqlalchemy_utils import database_exists
from os import path
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from functools import wraps
from .utilities.constants.constants import OAUTH2_CLIENT_SECRET
from flask_login import LoginManager

import logging
logger = logging.getLogger('waitress')

DB_NAME = "database.db"
db = SQLAlchemy()
botdb = SQLAlchemy()
api = Api()
jwt = JWTManager()
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
# SQLALCHEMY_TRACK_MODIFICATIONS = False
if not (os.environ.get('DEBUG_MODE') == 'True'):
    print('Running in production mode!')
    POSTGRES_URL = "postgres-viperaveilapi.postgres.svc.cluster.local:5435"
    POSTGRES_USER = "viperaveilapi"
    POSTGRES_PW = "7xwlf2r08mhz"
    POSTGRES_DB = "viperaveilapi"
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    POSTGRES_URL2 = "postgres-viperaveil.postgres.svc.cluster.local:5434"
    POSTGRES_USER2 = "viperaveil"
    POSTGRES_PW2 = "7xwlf2r08mhz"
    POSTGRES_DB2 = "viperaveil"
    DB_URL2 = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER2, pw=POSTGRES_PW2, url=POSTGRES_URL2, db=POSTGRES_DB2)
else:
    print('Running in development mode!')
    # DB_URL = f'sqlite:///{DB_NAME}'
    # DB_NAME = "database.db"
    # DB_URL = f'sqlite+aiosqlite:///{DB_NAME}'
    POSTGRES_URL = '10.40.0.80:5435'
    POSTGRES_USER = "viperaveilapi"
    POSTGRES_PW = "7xwlf2r08mhz"
    POSTGRES_DB = "viperaveilapi"
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)
    POSTGRES_URL2 = "10.40.0.80:5434"
    POSTGRES_USER2 = "viperaveil"
    POSTGRES_PW2 = "7xwlf2r08mhz"
    POSTGRES_DB2 = "viperaveil"
    DB_URL2 = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
        user=POSTGRES_USER2, pw=POSTGRES_PW2, url=POSTGRES_URL2, db=POSTGRES_DB2)


# compress = Compress()

def create_app():
    app = Flask(__name__)
    # Compress(app)
    app.config['SECRET_KEY'] = '39bac151af2292405a230a98fac0c554992963fe23937821fe05f8ddabc0f21e0e03416a3b41cb9783afc34178139d6a172bf8979dec5ca6b4a91f1dbff6cd43'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL  # f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_BINDS'] = {'db2': DB_URL2}
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SECRET_KEY'] = OAUTH2_CLIENT_SECRET
    db.init_app(app)
    #botdb.init_app(app)
    migrate = Migrate(app, db)
    # api.init_app(app, authorizations=authorizations, static_url_path='/static')
    jwt.init_app(app)

    # from .views import views
    # from .uploads import uploads
    from .auth import authBlueprint, authNS, auth
    # from .apiroute import index, rsiuserList, rsiuserSearch, rsiLink
    # from .bot import bot
    from .api import apiBlueprint, api, rsiNS, viperaNS, externalNS, eventNS
    from .bot import bot
    from .discordauth import discordauth
    from .ipc import ipc
    from .webhooks import webhooks, webhooksNS

    api.add_namespace(authNS)
    api.add_namespace(rsiNS)
    api.add_namespace(viperaNS)
    api.add_namespace(externalNS)
    api.add_namespace(eventNS)
    api.add_namespace(webhooksNS)

    app.register_blueprint(authBlueprint, url_prefix='/auth')
    app.register_blueprint(apiBlueprint, url_prefix='/api')
    app.register_blueprint(bot, url_prefix='/')
    app.register_blueprint(discordauth, url_prefix='/discord')
    app.register_blueprint(ipc, url_prefix='/ipc')
    app.register_blueprint(webhooks, url_prefix='/webhooks')

    # app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(api, url_prefix='/api/v1')

    from .models import apiUser, discordUser, rsiUser, rsiOrg, viperaUser, discordAccount

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'discord.index'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return discordAccount.query.get(id)

    return app

# Google Analytics - NOT IN USE.....YET
# SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
# KEY_FILE_LOCATION = 'acwebsite-347414-611159314a9a.json'

# Build Database if needed


def create_database(app):
    with app.app_context():
        if (os.environ.get('DEBUG_MODE') == 'True'):
            if not path.exists('website/' + DB_NAME):
                db.create_all()
                print('Created Database - devmode')
        if not database_exists(DB_URL):
            db.create_all()
            print('Created Database - Mainthread db build')
        if database_exists(DB_URL):
            from sqlalchemy import create_engine, inspect
            from sqlalchemy import MetaData, Table, Column, Text
            engine = create_engine(DB_URL)
            meta = MetaData()
            meta.bind = engine
            inspector = inspect(engine)
            if not inspector.has_table('apiUser'):
                db.create_all()
                print('Created tables!')
