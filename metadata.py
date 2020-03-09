import glob
import os

import requests
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3

import artwork
import utils


class Metadata:
    def __init__(self):
        self.label = ''
        self.country = ''
        self.realese_date = ''
        self.genre = ''
        self.style = ''
        self.image = ''

    def search_tags(self, music_title, artist=None):
        if artist:
            search_url = 'https://www.discogs.com/search/?q=' + utils.string_to_querystring(
                music_title + ' ' + artist) + '&type=release'
        else:
            search_url = 'https://www.discogs.com/search/?q=' + utils.string_to_querystring(
                music_title) + '&type=release'
        base_url = 'https://www.discogs.com'
        r = requests.get(search_url)
        base_soup = BeautifulSoup(r.content, 'html.parser')

        cards = base_soup.find_all('div', attrs={'class': 'card'})

        # find related card
        card = None
        for c in cards:
            card_artist = c.find('h5').text
            if utils.strip_text(artist.lower()) in utils.strip_text(card_artist.lower()):
                card = c
                break
        if not card:
            return

        card_href = card.find('a').get('href')
        song_link = base_url + card_href

        # download artwork
        artwork.download_artwork_discogs(song_link)

        song_page_r = requests.get(song_link)
        soup = BeautifulSoup(song_page_r.content, 'html.parser')

        # get informations
        all_divs = soup.find_all('div', attrs={'class': 'content'})
        texts = []
        for div in all_divs:
            # Label: # Format:# Country:# Released:# Genre:# Style:
            texts.append(utils.strip_text(div.text))

        self.label = texts[0]
        self.country = texts[2]
        self.realese_date = texts[3]
        self.genre = texts[4]
        self.style = texts[5]

    def edit_tags(self, path):
        audio = EasyID3(path)
        audio["title"] = self.label
        audio["releasecountry"] = self.country
        audio["date"] = utils.extract_date(self.realese_date)
        audio["genre"] = self.genre
        audio.save()


def create_metadata(directory, music_title, artist=None):
    music_directories = glob.glob(directory + "/*.mp3")
    path = ''

    for music_directory in music_directories:
        if music_title.lower() in music_directory.lower():
            path = music_directory
            break
    if path != '':
        metadata = Metadata()

        if artist:
            metadata.search_tags(music_title, artist)

        else:
            metadata.search_tags(music_title)

        # Paste
        metadata.edit_tags(path)

        if os.path.exists(utils.downloaded_image_path):
            artwork.edit_artwork(audio_path=path, picture_path=utils.downloaded_image_path)
            # Remove Downloaded Image if exist
            os.remove(utils.downloaded_image_path)
