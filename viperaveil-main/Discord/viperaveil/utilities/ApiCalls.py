import requests
from requests.structures import CaseInsensitiveDict
import json
from viperaveil.utilities.Constants import TempBotCredentials, SnekBackendEndpoint

# RSI API Lookups

def get_rsi_account(nickname):
    r = requests.post(url='https://robertsspaceindustries.com/api/spectrum/member/info/nickname', headers={'Content-Type': 'application/json'}, json={'nickname': nickname})
    dict = json.loads(r.text)
    return dict

# Get Token

def getVVToken():
    r = requests.post(
        f'{SnekBackendEndpoint}/auth/token',
        headers={
            'Content-Type': 'application/json'},
        json=TempBotCredentials)
    dict = json.loads(r.text)
    return dict['token']


def getBearerHeader():
    token = getVVToken()
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = f"Bearer {token}"
    return headers

# USER CRUD

def get_tt_latest_vid(id):
    try:
        raw = requests.get(
            f"{SnekBackendEndpoint}/external/tiktok/{id}",
            headers=getBearerHeader())
        r = json.loads(raw.text)
        return r
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

def GetRSIUser(id):
    try:
        raw = requests.get(
            f"{SnekBackendEndpoint}/rsi/user/{id}",
            headers=getBearerHeader())
        r = json.loads(raw.text)
        return r
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def GetRSIOrg(id):
    try:
        raw = requests.get(
            f"{SnekBackendEndpoint}/rsi/org/{id}",
            headers=getBearerHeader())
        r = json.loads(raw.text)
        return r
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def GetRSIBio(id):
    try:
        raw = requests.get(
            f"{SnekBackendEndpoint}/vipera/link/{id}",
            headers=getBearerHeader())
        r = json.loads(raw.text)
        return r
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def GetViperaUser(id):
    try:
        raw = requests.get(
            f"{SnekBackendEndpoint}/vipera/user/{id}",
            headers=getBearerHeader())
        r = json.loads(raw.text)
        return r
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def ListViperaUsers():
    try:
        r = requests.get(
            f"{SnekBackendEndpoint}/vipera/user",
            headers=getBearerHeader())
        return r.text
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def CreateViperaUser(newUserData):
    try:
        r = requests.put(
            f"{SnekBackendEndpoint}/vipera/user",
            json=newUserData,
            headers=getBearerHeader())
        return r.text
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def UpdateViperaUser(updateUserData):
    try:
        r = requests.post(
            f"{SnekBackendEndpoint}/vipera/user",
            json=updateUserData,
            headers=getBearerHeader())
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)


def DeleteViperaUser(id):
    try:
        r = requests.delete(
            f"{SnekBackendEndpoint}/vipera/user/{id}",
            headers=getBearerHeader())
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)
