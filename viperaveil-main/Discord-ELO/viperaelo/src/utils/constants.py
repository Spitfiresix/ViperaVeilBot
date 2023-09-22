import os

INIT_CHANNEL = 'init'
MODERATORS = 'moderators'
INFO_CHAT = 'info_chat'
REGISTER = '💬・lobby'
LOBBY = '💬・lobby'
SUBMIT = 'submit'
GAME_ANNOUNCEMENT = 'match_announcement'
BANS = 'bans'
ANNOUNCEMENTS = 'announcements'
QUEUE = 'Queue'

#Role
ADMIN_ROLE = 'Vipera Pick Up'

#catagories
SNEKWARS = '・─ 🐍 Snek Wars ⚔ ─・'
SNEKPICKUPS = 'Snek Wars'
SOLOELO = 'Solo'
TEAMSELO = 'Teams elo'


def getBaseUrlEndpoint():
    if not (os.environ.get('DEBUG_MODE') == 'True'):
        ENDPOINT = os.getenv('API_ENDPOINT')
    else:
        ENDPOINT = os.getenv('DEV_API_ENDPOINT')

    return ENDPOINT