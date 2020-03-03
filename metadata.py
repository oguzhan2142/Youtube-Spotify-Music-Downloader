from bs4 import BeautifulSoup
import requests
import os
import utils
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import youtube
import glob


class Metadata:
    def __init__(self):
        self.label = ''
        self.country = ''
        self.realese_date = ''
        self.genre = ''
        self.style = ''
        self.image = ''

    def pull_informations(self, query):
        search_url = 'https://www.discogs.com/search/?q=' + utils.string_to_querystring(query) + '&type=release'
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
            print('resim url:', pic['src'])
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
            texts.append(utils.strip_text(div.text))

        self.label = texts[0]
        self.country = texts[2]
        self.realese_date = texts[3]
        self.genre = texts[4]
        self.style = texts[5]

    def import_image_to_mp3(self, audio_path, picture_path):
        audio = MP3(audio_path, ID3=ID3)
        # adding ID3 tag if it is not present
        try:
            audio.add_tags()
        except error:
            pass
        audio.tags.add(APIC(
            mime='image/jpeg',
            type=3, desc=u'Cover',
            data=open(picture_path, 'rb').read())
        )
        # edit ID3 tags to open and read the picture from the path specified and assign it
        audio.save()  # save the current changes

    def import_tags_to_mp3(self, path):
        audio = EasyID3(path)
        audio["title"] = self.label
        audio["releasecountry"] = self.country
        audio["date"] = utils.extract_date(self.realese_date)
        audio["genre"] = self.genre
        # audio["title"] = u"An example"
        # print('date:', type(audio.))
        audio.save()


def paste_metadata(directory, track_name):
    music_directories = glob.glob(directory + "/*.mp3")
    path = ''

    for dir in music_directories:
        if track_name.lower() in dir.lower():
            path = dir
            break
    if path != '':
        metadata = Metadata()
        metadata.pull_informations(track_name)
        metadata.import_tags_to_mp3(path)
        metadata.import_image_to_mp3(audio_path=path, picture_path='img.jpg')
        os.remove('img.jpg')
