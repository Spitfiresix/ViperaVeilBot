import requests
from bs4 import BeautifulSoup
from datetime import datetime


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
                playerEnlistedDateRaw = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.left-col > div > p:nth-child(1) > strong').text
                playerEnlistedDate = datetime.strptime(
                    playerEnlistedDateRaw, "%b %d, %Y")
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
                playerAvatar = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.profile.left-col > div > div.thumb > img')['src']
                if not 'robertsspaceindustries.com' in playerAvatar:
                    if not 'https://robertsspaceindustries.com' in playerAvatar:
                        playerAvatar = 'https://robertsspaceindustries.com' + playerAvatar
            except BaseException:
                playerAvatar = None
            try:
                playerBadge = parsedData.select_one(
                    '#public-profile > div.profile-content.overview-content.clearfix > div.box-content.profile-wrapper.clearfix > div > div.profile.left-col > div > div.info > p:nth-child(3) > span.icon > img')['src']
                if not 'robertsspaceindustries.com' in playerBadge:
                    if not 'https://robertsspaceindustries.com' in playerBadge:
                        playerBadge = 'https://robertsspaceindustries.com' + playerBadge
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
                    orgResp = requests.get(playerMainOrgLink, stream=True)
                    orgData = orgResp.text
                    parsedOrgData = BeautifulSoup(orgData, "lxml")
                    str_member_count = parsedOrgData.select_one('#organization > div > div.content-wrapper > div.heading > div.inner > div > span').text
                    orgMembers = str_member_count.replace(' members','')
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
        elif apiLoc == 'org':
            Url = f'https://robertsspaceindustries.com/orgs/{inputData}'
            Resp = requests.get(Url, stream=True)
            if Resp.status_code != 200:
                return 'Player does not exist'
            Data = Resp.text
            parsedData = BeautifulSoup(Data, 'lxml')

            try:
                mainOrgIcon = 'https://robertsspaceindustries.com' + parsedData.select_one(
                    '#organization > div > div.content-wrapper > div.heading > div.inner > div > img')['src']
            except BaseException:
                mainOrgIcon = None
            try:
                mainOrgSID = parsedData.select_one(
                    '#organization > div > div.content-wrapper > div.heading > div.inner > h1 > span').text
            except BaseException:
                mainOrgSID = None
            try:
                mainOrgNameData = parsedData.select_one(
                    '#organization > div > div.content-wrapper > div.heading > div.inner > h1').text
                mainOrgName = mainOrgNameData.replace(f' / {mainOrgSID}', '')
            except BaseException:
                mainOrgName = None
            try:
                orgTagsData = parsedData.select_one(
                    '#organization > div > div.content-wrapper > div.heading > div.inner > ul.tags.clearfix')
                orgTagsLi = orgTagsData.find_all('li')
                orgTags = []
                for li in orgTagsLi:
                    orgTags.append({
                        'class': li['class'][0].upper(),
                        'text': li.text
                    })
            except BaseException:
                orgTags = None

            orgUrl = Url + '/members'
            orgResp = requests.get(orgUrl, stream=True)
            orgData = orgResp.text
            parsedOrgData = BeautifulSoup(orgData, "lxml")
            orgMembersData = parsedOrgData.select_one('#members-data')
            orgMembers = len(
                orgMembersData.find_all(
                    'a', class_='membercard js-edit-member'))

            orgDict = {'data': {
                'organization': {
                    'url': Url,
                    'image': mainOrgIcon,
                    'name': mainOrgName,
                    'sid': mainOrgSID,
                    'members': orgMembers,
                    'tags': orgTags
                }
            }}
            return orgDict
    return 'Player does not exist'
