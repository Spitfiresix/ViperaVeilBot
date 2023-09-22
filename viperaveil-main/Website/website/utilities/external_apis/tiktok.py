
import requests
from bs4 import BeautifulSoup

def tt_latest_lookup(inputData):
    Url = f'https://www.tiktok.com/@{inputData}'
    headers = {"user-agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    Resp = requests.get(Url, headers=headers, stream=True)
    Data = Resp.text
    parsedData = BeautifulSoup(Data, 'lxml')
    profile_img_url = parsedData.select_one('#main-content-others_homepage > div > div.tiktok-1g04lal-DivShareLayoutHeader-StyledDivShareLayoutHeaderV2.enm41492 > div.tiktok-1gk89rh-DivShareInfo.ekmpd5l2 > div.tiktok-uha12h-DivContainer.e1vl87hj1 > span > img')['src']
    #latest_vid_url = parsedData.select_one('#main-content-others_homepage > div > div.tiktok-833rgq-DivShareLayoutMain.ee7zj8d4').select_one('a')['href']
    latest_vid_url = parsedData.select('.tiktok-1s72ajp-DivWrapper')[0].select('a')[0]['href']
    #main-content-others_homepage > div > div.tiktok-833rgq-DivShareLayoutMain.ee7zj8d4 > div.tiktok-1qb12g8-DivThreeColumnContainer.eegew6e2 > div > div:nth-child(1) > div.tiktok-x6f6za-DivContainer-StyledDivContainerV2.eq741c50 > div > div > a
    title = parsedData.findAll('div', attrs={'class': 'tiktok-5lnynx-DivTagCardDesc'})[0].select_one('a')['title']
    data = {'data': {
                'profile': {
                    'image': profile_img_url
                    },
                'latest_vid': {
                    'id': latest_vid_url.split("/")[-1],
                    'title': title,
                    'url': latest_vid_url
                    }
                }
            }
    return data