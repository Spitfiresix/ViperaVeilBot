from flask import Blueprint
from flask_restx import Resource, Api
from threading import Thread

import logging
logger = logging.getLogger('waitress')

ipc = Blueprint('ipc', __name__)


@ipc.route('/')
async def index():
    return 'ipc root'
    member_count = await ipcClient.request(
        "get_member_count", guild_id=303245408539246603
    )  # get the member count of server with ID 12345678

    return str(member_count)  # display member count
