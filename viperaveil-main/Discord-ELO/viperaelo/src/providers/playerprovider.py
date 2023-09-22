from src.modules.player import Player
from src.utils.constants import getBaseUrlEndpoint
import requests
import json

base_url = f"{getBaseUrlEndpoint()}/api/players"

def add_player(player):
    response = requests.post(f"{base_url}/add", json=player)
    return response.status_code == 200

def get_players():
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_player(id):
    response = requests.get(f"{base_url}/{id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def remove_player(player_name):
    response = requests.delete(f"{base_url}/{player_name}")
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        return None