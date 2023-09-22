import json
import requests
from website.utilities.constants.constants import BOT_API


def get_discord_staff():
    try:
        raw = requests.get(f"{BOT_API}/async/discord/staff")
        r = json.loads(raw.text)
        return r
    except:
        pass

def get_discord_devs():
    try:
        raw = requests.get(f"{BOT_API}/async/discord/devs")
        r = json.loads(raw.text)
        return r
    except:
        pass

def post_discord_event(endpoint, payload):
    try:
        raw = requests.post(f"{BOT_API}/discord/webhook?endpoint={endpoint}", data=payload, headers={'Content-Type':'application/xml; charset=UTF-8'})
        return raw
    except:
        pass