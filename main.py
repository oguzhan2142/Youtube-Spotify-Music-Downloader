import requests
import youtube_dl
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from screen import Screen


def download_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


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


def start_download():
    youtube_url = 'https://www.youtube.com'
    music_names = give_names_spotify()
    status_string = ''
    for music in music_names:
        results = YoutubeSearch(music, max_results=1).videos
        first_result = results[0]
        first_result_link = first_result['link']
        status_string += (music + ' downloading' + '\n')
        screen.status.set(screen.status.get() + ' aa ')
        download_mp3(youtube_url + first_result_link)
        break


def asd():
    screen.status.set(screen.status.get() + ' ok \n')


if __name__ == '__main__':
    screen = Screen()
    screen.status.set('Waiting For Link')
    screen.B.configure(command=asd)
    screen.screen_show()
