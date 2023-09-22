import requests
from datetime import datetime
from src.utils.constants import getBaseUrlEndpoint

base_url = f"{getBaseUrlEndpoint()}/api/Ban"
def add_ban(ban):

    values = {
        "UserId": ban["UserId"],
        "DateNow": ban["DateNow"].isoformat(),
        "TimeEnd": ban["TimeEnd"].isoformat(),
        "Reason": ban["Reason"]
    }

    response = requests.post(base_url, json=values)

    if response.status_code == 200:
        print("Ban added successfully")
    else:
        print("Failed to add ban")

def get_bans():

    response = requests.get(base_url)

    if response.status_code == 200:
        bans = response.json()
        return bans
    else:
        print("Failed to get bans")
        return []

def unban_user(user_id):
    endpoint = f"{getBaseUrlEndpoint()}/{user_id}/unban"

    response = requests.post(endpoint)

    if response.status_code == 200:
        print("User unbanned successfully")
    else:
        print("Failed to unban user")
