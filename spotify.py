from threading import Thread
import requests
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from youtube import download_mp3


def download_from_spotify(screen):
    youtube_url = 'https://www.youtube.com'
    music_names = give_names_spotify()
    for music in music_names:
        first_result = YoutubeSearch(music, max_results=1).videos[0]
        if not first_result:
            screen.append_text('None Value Cannot Downloaded\n')
            continue
        first_yt_link = first_result['link']
        screen.append_text(music + ' downloading' + '\n')
        download_link = youtube_url + first_yt_link
        Thread(target=download_mp3, args=(download_link, screen,)).start()


def give_names_spotify():
    r = requests.get('https://open.spotify.com/playlist/7IImK40Rng4pclYflKPLs9')
    soup = BeautifulSoup(r.content, 'html.parser')

    divs = soup.find_all('div', attrs={'class': 'tracklist-col name'})
    track_names = []
    for link in divs:
        track_name = link.find('span', attrs={'class': 'track-name'})
        # artists_albums = link.find('span', attrs={'class': 'artists-albums'})
        track_names.append(track_name.text)
    return track_names
