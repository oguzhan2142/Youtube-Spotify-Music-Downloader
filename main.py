import requests
import youtube_dl
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from screen import Screen
from threading import Thread
import time


def download_mp3(url):
    def my_hook(d):
        if d['status'] == 'error':
            screen.append_text('error occured\n')
        if d['status'] == 'finished':
            screen.append_text(d['filename'] + ' finished...\n')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
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
    screen.append_text('Downloads Starting...\n')

    for index, music in enumerate(music_names):
        first_result = YoutubeSearch(music, max_results=1).videos[0]

        if not first_result:
            screen.append_text('None Value Cannot Downloaded\n')
            continue

        first_yt_link = first_result['link']
        screen.append_text(music + ' downloading' + '\n')
        download_link = youtube_url + first_yt_link
        Thread(target=download_mp3, args=(download_link,)).start()


if __name__ == '__main__':
    screen = Screen()
    screen.status.set('Waiting For Link')
    screen.B.configure(command=lambda: Thread(target=start_download).start())
    screen.screen_show()
