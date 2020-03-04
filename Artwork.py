from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def save_image(image_query):
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome('Driver/MacOs/chromedriver', options=chrome_options)

    driver.get('https://www.google.com.tr/imghp?hl=tr&tab=wi&ogbl')
    inputbox = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    inputbox.send_keys(image_query)
    inputbox.send_keys(Keys.ENTER)
    first_img = driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
    first_img.screenshot('img.jpg')
