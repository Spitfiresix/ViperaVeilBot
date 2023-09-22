import requests
from bs4 import BeautifulSoup
import random
import string

# SCAPIKey = 'e23d2375f7fc2de37dd1fed9be43cf6d'

# def apiLookup(inputData : str, apiLoc : str):
#     """Requires input data, this is a str of the user handle/org ticker.
# Will return url associated with user/org/orgMembers with api filled in
# as str."""

#     if apiLoc == 'user':
#         Url = f'https://api.starcitizen-api.com/{SCAPIKey}/v1/eager/user/{inputData}'
#     elif apiLoc == 'org':
#         Url = f'https://api.starcitizen-api.com/{SCAPIKey}/v1/eager/organization/{inputData}'
#     elif apiLoc == 'orgMem':
#         Url = f'https://api.starcitizen-api.com/{SCAPIKey}/v1/live/organization_members/{inputData}'
#     else:
#         return 'Incorrect apiLoc submitted!'
#     Resp = requests.get(Url, stream=True)
#     Data = Resp.text
#     return Data

pendingAuth = []
playerDict = {
    'handle': None,
    'discord': None,
    'key': None
}


def getVVUser(handle: str = None, discord: str = None, key: str = None):
    for records in pendingAuth:
        if handle == records['handle']:
            return records
        if discord == records['discord']:
            return records
        if key == records['key']:
            return records
        else:
            return None


def addVVUser(handle: str, discord: str, key: str):
    pendingUserDict = {
        'handle': handle,
        'discord': discord,
        'key': key
    }
    try:
        pendingAuth.append(pendingUserDict)
        return None
    except BaseException:
        return 'Error'


def setVVUser(handle: str, discord: str, key: str):
    for records in pendingAuth:
        if discord == records['discord']:
            records['handle'] = handle
            records['key'] = key
            return records
        else:
            return None


def getKey():
    """Generate a random key"""
    str = string.ascii_lowercase + '0' + '1' + \
        '2' + '3' + '4' + '5' + '6' + '7' + '8' + '9'
    return ''.join(random.choice(str) for i in range(12))


def apiRSILookup(inputData: str = None, apiLoc: str = None):
    """Requires input data, this is a str of the users handle/org ticker.
    Will return dict associated with user/org/orgMembers.
    ### CALLING THIS MULTIPLE TIMES WILL EXPONENTIALLY INCREASE LOAD TIME
    Due to the time it takes to retrieve data from rsi.com."""
    userData = {}
    if inputData:
        if apiLoc == 'user':
            Url = f'https://robertsspaceindustries.com/citizens/{inputData}'
            Resp = requests.get(Url, stream=True)
            if Resp.status_code != 200:
                return 'Player does not exist'
            Data = Resp.text
            parsedData = BeautifulSoup(Data, 'lxml')
            try:
                playerHandle = parsedData.select_one(
                    'div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.profile.left-col > div > div.info > p:nth-child(2) > strong').text
            except BaseException:
                playerHandle = None
            try:
                playerDisplayName = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.profile.left-col > div > div.info > p:nth-child(1) > strong').text
            except BaseException:
                playerDisplayName = None
            try:
                playerRecordID = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > p > strong').text
            except BaseException:
                playerRecordID = None
            try:
                playerEnlistedDate = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.left-col > div > p:nth-child(1) > strong').text
            except BaseException:
                playerEnlistedDate = None
            try:
                playerFluency = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.left-col > div > p:nth-child(3) > strong').text.strip()
            except BaseException:
                try:
                    playerFluency = parsedData.select_one(
                        '#public-profile > div.profile-content.overview-content.clearfix > div.left-col > div > p:nth-child(2) > strong').text.strip()
                except BaseException:
                    playerFluency = None
            try:
                playerWebsite = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.right-col > div > p > a').text
            except BaseException:
                playerWebsite = None
            try:
                playerAvatar = 'https://robertsspaceindustries.com' + parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.profile.left-col > div > div.thumb > img')['src']
            except BaseException:
                playerAvatar = None
            try:
                playerBadge = 'https://robertsspaceindustries.com' + parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.profile.left-col > div > div.info > p:nth-child(3) > span.icon > img')['src']
            except BaseException:
                playerBadge = None
            try:
                playerBadgeName = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.profile.left-col > div > div.info > p:nth-child(3) > span.value').text
            except BaseException:
                playerBadgeName = None
            try:
                playerBio = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.right-col > div > div > div').text
            except BaseException:
                playerBio = None
            try:
                playerMainOrgName = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.main-org.right-col.visibility-V > div > div.info > p:nth-child(1) > a').text
            except BaseException:
                playerMainOrgName = None
            try:
                playerMainOrgLink = 'https://robertsspaceindustries.com' + parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.main-org.right-col.visibility-V > div > div.info > p:nth-child(1) > a')['href']
            except BaseException:
                playerMainOrgLink = None
            try:
                playerMainOrgIcon = 'https://robertsspaceindustries.com' + parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.main-org.right-col.visibility-V > div > div.thumb > a > img')['src']
            except BaseException:
                playerMainOrgIcon = None
            try:
                playerMainOrgSID = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.main-org.right-col.visibility-V > div > div.info > p:nth-child(2) > strong').text
            except BaseException:
                playerMainOrgSID = None
            try:
                playerMainOrgRank = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.main-org.right-col.visibility-V > div > div.info > p:nth-child(3) > strong').text
            except BaseException:
                playerMainOrgRank = None
            try:
                playerMainOrgStarsData = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.main-org.right-col.visibility-V > div > div.info > div').find_all('span', class_='active')
                playerMainOrgStars = 0
                for stars in playerMainOrgStarsData:
                    playerMainOrgStars += 1
                if playerMainOrgLink:
                    orgUrl = playerMainOrgLink + '/members'
                    orgResp = requests.get(orgUrl, stream=True)
                    orgData = orgResp.text
                    parsedOrgData = BeautifulSoup(orgData, "lxml")
                    orgMembersData = parsedOrgData.select_one('#members-data')
                    orgMembers = len(
                        orgMembersData.find_all(
                            'a', class_='membercard js-edit-member'))
            except BaseException:
                playerMainOrgStars = None
                orgMembers = None
        userDict = {'data': {
            'affiliation': {
            },
            'organization': {
                'image': playerMainOrgIcon,
                'name': playerMainOrgName,
                'rank': playerMainOrgRank,
                'sid': playerMainOrgSID,
                'stars': playerMainOrgStars,
                'members': orgMembers
            },
            'profile': {
                'badge': playerBadgeName,
                'badge_image': playerBadge,
                'bio': playerBio,
                'display': playerDisplayName,
                'enlisted': playerEnlistedDate,
                'fluency': playerFluency,
                'handle': playerHandle,
                'id': playerRecordID,
                'image': playerAvatar,
                'website': playerWebsite,
                'page': {
                    'title': f'{playerHandle} | {playerDisplayName}',
                    'url': f'https://robertsspaceindustries.com/citizens/{playerHandle}'
                }
            },
        }}
        return userDict
    return 'Player does not exist'
