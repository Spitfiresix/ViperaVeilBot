
from src.utils.constants import getBaseUrlEndpoint
import requests

base_url = f"{getBaseUrlEndpoint()}/api/leaderboard"
# Function to add a player to the leaderboard
def add_player_to_leaderboard(player_name, score, game_mode):
    url = f"{base_url}/add"
    data = {
        "playerName": player_name,
        "score": score,
        "gameMode": game_mode
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Player added to the leaderboard successfully.")
    else:
        print("Failed to add player to the leaderboard.")

# Function to get the leaderboard for a specific game mode
def get_leaderboard(game_mode):
    url = f"{base_url}/{game_mode}"
    response = requests.get(url)
    if response.status_code == 200:
        leaderboard = response.json()
        print(f"Leaderboard for {game_mode}:")
        for rank, player in enumerate(leaderboard, start=1):
            player_name = player["playerName"]
            score = player["score"]
            print(f"{rank}. {player_name} - Score: {score}")
        return leaderboard
    else:
        print("Failed to retrieve the leaderboard.")