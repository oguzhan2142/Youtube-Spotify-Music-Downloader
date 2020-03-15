import platform
import shutil
import time

import requests
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import utils
from bs4 import BeautifulSoup


def download_artwork_google(image_query):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    if platform.system() == 'Windows':
        driver = webdriver.Chrome('Driver/Windows/chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('Driver/MacOs/chromedriver', options=chrome_options)

    driver.get('https://www.google.com.tr/imghp?hl=tr&tab=wi&ogbl')
    inputbox = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    inputbox.send_keys(image_query + ' artwork')
    inputbox.send_keys(Keys.ENTER)
    first_img = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
    first_img.screenshot(utils.downloaded_image_path)
    driver.quit()
    print('google gorseller kullandim query : ', image_query)


def download_artwork_discogs(url):
    now = int(round(time.time() * 1000))
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")

    if platform.system() == 'Windows':
        driver = webdriver.Chrome('Driver/Windows/chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('Driver/MacOs/chromedriver', options=chrome_options)

    driver.get(url)
    img = driver.find_element_by_xpath('//*[@id="page_content"]/div[1]/div[1]/a/span[2]/img')
    img.screenshot(utils.downloaded_image_path)
    last = int(round(time.time() * 1000))
    driver.quit()
    print('time diff artwork:', (last - now) / 1000, ' sec')


def download_discord(url):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(utils.downloaded_image_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def edit_artwork(audio_path, picture_path):
    audio = MP3(audio_path, ID3=ID3)
    # adding ID3 tag if it is not present
    # try:
    #     audio.add_tags()
    # except error:
    #     pass

    try:
        audio.tags.add(APIC(
            mime='image/jpeg',
            type=3, desc=u'Cover',
            data=open(picture_path, 'rb').read())
        )
    except FileNotFoundError:
        print('IMG file not found')
    # edit ID3 tags to open and read the picture from the path specified and assign it
    audio.save()  # save the current changes
