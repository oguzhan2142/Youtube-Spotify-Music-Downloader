import platform

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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


def get_metadata(song_name='her sey fani'):
    base_url = 'https://www.discogs.com/'
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")

    if platform.system() == 'Windows':
        driver = webdriver.Chrome('Driver/Windows/chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('Driver/MacOs/chromedriver', options=chrome_options)
    driver.get(base_url)
    search_box = driver.find_element_by_xpath('//*[(@id = "search_q")]')
    search_box.send_keys(song_name)
    search_btn = driver.find_element_by_xpath(
        '//*[(@id = "do_site_search")]')
    search_btn.click()
    print(BeautifulSoup(driver.page_source, 'html.parser').text)

    soup = BeautifulSoup(driver.page_source.encode("utf-8"), 'html.parser')

    driver.quit()


get_metadata('her sey fani')
