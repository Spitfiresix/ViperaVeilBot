
from src.utils.constants import getBaseUrlEndpoint
from discord import Game
import requests
import pickle   
import codecs
import base64

# # Base URL of the API
# base_url = f"{getBaseUrlEndpoint()}/api/game"
  
# def get_games(endpoint, id):
#     response = requests.get(f"{endpoint}/api/game/{id}")
#     if response.status_code == 200:
#         # The request was successful
#         b = response.content
#         return retrieve_and_deserialize(b)
        
#     else:
#         # The request failed
#         return None

# def create_game(endpoint,id, data):
#     newData = serialize_and_store(data)   
#     headers = {'Content-Type': 'application/octet-stream'}  # Specify that the payload is binary data

#     response = requests.post(f"{endpoint}/api/game/{id}", headers=headers, data=newData)
#     if response.status_code == 200:
#         # The request was successful
#         print(f"New Game Created")
#     else:
#         # The request failed
#         print(f"Request failed with status code {response.status_code}")

# def update_game(endpoint, id, data):
#     newData = serialize_and_store(data)
#     response = requests.put(f"{endpoint}/api/game/{id}", json=newData)
#     if response.status_code == 200:
#         # The request was successful
#         print(f"Game Updated")
#     else:
#         # The request failed
#         print(f"Request failed with status code {response.status_code}")


