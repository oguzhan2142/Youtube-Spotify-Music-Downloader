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


def get_metadata(song_name='her sey fani'):
    base_url = 'https://www.discogs.com/search/?q=' + query('her sey fani') + '&type=all'
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")

    if platform.system() == 'Windows':
        driver = webdriver.Chrome('Driver/Windows/chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('Driver/MacOs/chromedriver', options=chrome_options)
    driver.get(base_url)
    first_result = driver.find_element_by_class_name('search_result_title')
    first_result.click()
    soup = BeautifulSoup(driver.page_source.encode("utf-8"), 'html.parser')
    pic_span = soup.find('span', attrs={'class': 'thumbnail_center'})
    pic = pic_span.find_next('img')

    # Save Image
    page = requests.get(pic['src'])
    f_ext = os.path.splitext(pic['src'])[-1]
    f_name = 'img{}'.format(f_ext)
    with open(f_name, 'wb') as f:
        f.write(page.content)

    # get informations
    all_divs = soup.find_all('div', attrs={'class': 'content'})
    texts = []
    for div in all_divs:
        # Label: # Format:# Country:# Released:# Genre:# Style:
        texts.append(extract_text(div.text))

    metadata = Metadata(label=texts[0], country=texts[2],
                        realase_date=texts[3], genre=texts[4],
                        style=texts[5]
                        )

    driver.quit()
