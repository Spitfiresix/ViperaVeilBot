from flask import Flask, Blueprint, request, jsonify, make_response
from flask_restx import Resource, Api, Namespace
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_manager
from . import db
from . import api
from .models import apiUser
import datetime
from functools import wraps

authBlueprint = Blueprint('auth', __name__)
auth = Api(
    authBlueprint,
    version='1.0',
    title='Vipera Veil API',
    description='Facilitating authentication')
# assert url_for('api.doc') == '/api/doc/'

authNS = Namespace(name='auth', description='For authenticating with the API')


@authNS.route('/token')
@authNS.doc(params={'username': 'An existing API Username',
            'password': 'An existing API Password'})
class Token(Resource):
    def get(self):
        # Get the user details from the request body
        if request.json:
            username = request.json['username']
            password = request.json['password']
        else:
            username = request.args['username']
            password = request.args['password']

        # Query Database for user
        user = db.session.query(apiUser).filter(
            apiUser.username == username and apiUser.password == password).first()

        # Generate an access token for the user
        if user:
            token = create_access_token(
                identity=user.id,
                fresh=True,
                expires_delta=datetime.timedelta(
                    seconds=120))

            return {'token': token}, 201
        else:
            return 'Username/password not valid', 401

    def post(self):
        # Get the user details from the request body
        if request.json:
            username = request.json['username']
            password = request.json['password']
        else:
            username = request.args['username']
            password = request.args['password']

        # Query Database for user
        user = db.session.query(apiUser).filter(
            apiUser.username == username and apiUser.password == password).first()

        # Generate an access token for the user
        if user:
            token = create_access_token(
                identity=user.id,
                fresh=True,
                expires_delta=datetime.timedelta(
                    seconds=120))

            return {'token': token}, 201
        else:
            return 'Username/password not valid', 401
