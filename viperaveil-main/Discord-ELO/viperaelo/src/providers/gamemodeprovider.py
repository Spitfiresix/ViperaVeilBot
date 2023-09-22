
from src.utils.constants import getBaseUrlEndpoint
import requests
import json 
# Base URL of the API
base_url = f"{getBaseUrlEndpoint()}/api/gamemodes"

# Function to add a game mode
def add_game_mode(game_mode):
    url = f"{base_url}/add/{game_mode}"
    response = requests.post(url)
    if response.status_code == 200:
        print("Game mode added successfully.")
    else:
        print("Failed to add game mode.")

# Function to get all game modes
def get_game_modes():
    url = base_url
    response = requests.get(url)
    if response.status_code == 200:
        game_modes = response.json()
        return game_modes
    else:
        print("Failed to retrieve game modes.")
def delete_game_mode(mode):
    url = base_url
    response = requests.delete(f"{base_url}/{mode}")
    
# # Example usage
# add_game_mode("1v1")
# add_game_mode("2v2")
# add_game_mode("3v3")
# get_game_modes()
