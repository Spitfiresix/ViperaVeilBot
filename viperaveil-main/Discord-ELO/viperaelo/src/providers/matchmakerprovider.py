
from src.utils.constants import getBaseUrlEndpoint
import requests

# Base URL of the API
base_url = f"{getBaseUrlEndpoint()}/api/matchmaking"

# Function to enqueue a player
def enqueue_player(player_name, game_modes):
    url = f"{base_url}/enqueue"
    data = {
        "playerName": player_name,
        "gameMode": game_modes
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Player enqueued successfully.")
    else:
        print("Failed to enqueue player.")

# Function to dequeue a player
def dequeue_player():
    url = f"{base_url}/dequeue"
    response = requests.post(url)
    if response.status_code == 200:
        print("Player dequeued successfully.")
    else:
        print("Failed to dequeue player.")
