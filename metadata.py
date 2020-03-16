import os

import requests
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3

import artwork
import utils


class Metadata:
    def __init__(self):
        self.label = ''
        self.format = ''
        self.album = ''
        self.country = ''
        self.realese_date = ''
        self.genre = ''
        self.style = ''
        self.image = ''

    def download_artwork(self, download_link):
        pass

    def search_tags(self, music_title, artist):

        if '(' in music_title and ')' in music_title:
            music_title = utils.remove_parantesis(music_title)

        album_search_url = 'https://www.discogs.com/search/?q=' + utils.string_to_querystring(
            music_title + ' ' + artist) + '&format_exact=Album&type=release'
        # search_url = 'https://www.discogs.com/search/?q=' + utils.string_to_querystring(
        #     music_title + ' ' + artist) + '&type=release'
        # print('search url:', album_search_url)
        base_url = 'https://www.discogs.com'
        r = requests.get(album_search_url)
        base_soup = BeautifulSoup(r.content, 'html.parser')

        # Parse albumname
        album_name_a = base_soup.find('a', attrs={'class': 'search_result_title'})

        if album_name_a:
            self.album = album_name_a.text
        else:
            # print('CD ariyor')
            cd_search_url = 'https://www.discogs.com/search/?q=' + utils.string_to_querystring(
                music_title + ' ' + artist) + '&format_exact=CD&type=release'
            r = requests.get(cd_search_url)
            base_soup = BeautifulSoup(r.content, 'html.parser')

            # Parse albumname
            album_name_a = base_soup.find('a', attrs={'class': 'search_result_title'})
            if album_name_a:
                self.album = album_name_a.text

        # print('album name: ',self.album)
        cards = base_soup.find_all('div', attrs={'class': 'card'})
        # find related card if artist exist
        card = None
        for c in cards:
            card_artist = c.find('h5').text
            # seperation for various artists
            if ',' in artist:
                artist = artist.split(',')[0]
            # print('artist:', utils.strip_text(artist.lower()))
            # print('card_artist:', utils.strip_text(card_artist.lower()))
            if utils.strip_text(artist.lower()) in utils.strip_text(card_artist.lower()):
                card = c
                break

        # if not card:
        #     artwork.download_artwork_google(music_title + ' ' + artist)
        #     return

        # print('CARD STATUS')
        if card:
            print('card exist')
        else:
            artwork.download_artwork_google(music_title + ' ' + artist)
            # print('card does not exist downloaded from google')
            return

        card_href = card.find('a').get('href')
        song_link = base_url + card_href

        song_page_r = requests.get(song_link)
        soup = BeautifulSoup(song_page_r.content, 'html.parser')

        # download artwork
        # parse img path
        img_span = soup.find(attrs={'class': 'thumbnail_center'})
        img = img_span.find_next()
        img_link = img['src']
        artwork.download_discord(img_link)
        # print('metadata song_link', song_link)

        # get informations
        all_divs = soup.find_all('div', attrs={'class': 'content'})
        texts = []
        for div in all_divs:
            # Label: # Format:# Country:# Released:# Genre:# Style:
            texts.append(utils.strip_text(div.text))

        self.label = music_title
        self.format = texts[1]
        self.country = texts[2]
        self.realese_date = texts[3]
        self.genre = texts[4]
        self.style = texts[5]
        # print('search path fonksiyonundan cikti')

    def edit_tags(self, path):
        audio = EasyID3(path)
        audio["title"] = self.label
        audio['album'] = self.album
        audio["releasecountry"] = self.country
        audio["date"] = utils.extract_date(self.realese_date)
        audio["genre"] = self.genre
        audio.save()


#
# m = Metadata()
# m.search_tags('Anason', 'Zakkum')


def create_metadata(path, music_title, artist):
    # print('create_metadata icine girdi')
    result = False
    metadata = Metadata()

    # Search tags and download Image

    metadata.search_tags(music_title, artist)

    # Paste tags
    try:
        metadata.edit_tags(path)
        if os.path.exists(utils.downloaded_image_path):
            artwork.edit_artwork(audio_path=path, picture_path=utils.downloaded_image_path)
            # Remove Downloaded Image if exist
            os.remove(utils.downloaded_image_path)
            result = True
        # print('create_metadatadan cikti')
    except:
        print('error inside create_metadata')
    return result
