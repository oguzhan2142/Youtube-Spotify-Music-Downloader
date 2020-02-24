from screen import Screen
from spotify import *
from youtube import *
import requests


def downloading_process():
    url = screen.E1.get()

    try:
        requests.get(url)
    except:
        screen.append_text('Invalid URL')
        return

    if 'https://www.youtube.com' in url:
        # youtube
        screen.append_text('Downloading from YouTube\n')
        download_from_yt(url, screen)
    elif 'https://open.spotify.com' in url:
        # spotify
        screen.append_text('Downloading from Spotify\n')
        download_from_spotify(url, screen)
    else:
        screen.append_text(url + ' Not Spotify or YouTube link')


if __name__ == '__main__':
    screen = Screen()
    screen.status.set('Waiting For Link')
    screen.B.configure(command=lambda: Thread(target=downloading_process).start())
    screen.screen_show()
