import requests
from bs4 import BeautifulSoup


def getImage(Url: str):
    image = Url.replace(
        'maxresdefault',
        'mqdefault').replace(
        'hqdefault',
        'mqdefault').replace(
            '500x500',
        '200x200')
    return image


def setText(text):
    if len(text) > 27:
        text = f'{text[0:27]}...'
    return text
