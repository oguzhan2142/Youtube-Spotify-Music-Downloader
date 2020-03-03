import platform

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import os


class Metadata:
    def __init__(self, label, country, realase_date, genre, style):
        self.label = label
        self.country = country
        self.realese_date = realase_date
        self.genre = genre
        self.style = style


def query(query='query'):
    arr = query.split(' ')
    if len(arr) > 1:
        modified = ''
        for index, a in enumerate(arr):
            modified += a
            if index == len(arr) - 1:
                continue
            modified += '+'
        return modified
    else:
        return query


def extract_text(string=''):
    string = string.replace('\n', '')
    string = string.strip()
    return string


def create_metadata_object(song_name='her sey fani'):
    search_url = 'https://www.discogs.com/search/?q=' + query(song_name) + '&type=release'
    base_url = 'https://www.discogs.com'
    print('search_url', search_url)
    r = requests.get(search_url)
    base_soup = BeautifulSoup(r.content, 'html.parser')

    cards = base_soup.find_all('div', attrs={'class': 'card'})
    first_box_href = cards[0].find('a').get('href')
    song_link = base_url + first_box_href
    song_page_r = requests.get(song_link)
    soup = BeautifulSoup(song_page_r.content, 'html.parser')
    pic_span = soup.find('span', attrs={'class': 'thumbnail_center'})
    pic = pic_span.find_next('img')

    # Save Image
    try:
        page = requests.get(pic['src'])
        f_ext = os.path.splitext(pic['src'])[-1]
        f_name = 'img{}'.format(f_ext)
        with open(f_name, 'wb') as f:
            f.write(page.content)
    except:
        print('resim alinamadi')
    # get informations
    all_divs = soup.find_all('div', attrs={'class': 'content'})
    texts = []
    for div in all_divs:
        # Label: # Format:# Country:# Released:# Genre:# Style:
        texts.append(extract_text(div.text))

    metadata_obj = Metadata(label=texts[0], country=texts[2],
                            realase_date=texts[3], genre=texts[4],
                            style=texts[5]
                            )
    return metadata_obj
