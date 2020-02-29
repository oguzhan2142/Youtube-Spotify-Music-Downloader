from screen import Screen
from spotify import *
from youtube import *
import requests


def downloading_process():
    url = screen.url_field.get()

    try:
        requests.get(url)
    except:
        screen.append_text('Invalid URL\n')
        return

    if 'https://www.youtube.com' in url:
        # youtube
        screen.append_text('Downloading from YouTube\n')
        if screen.directory:
            download_from_yt(url, screen, directory=screen.directory)
        else:
            download_from_yt(url, screen)
    elif 'https://open.spotify.com' in url:
        # spotify
        screen.append_text('Downloading from Spotify\n')
        if screen.directory:
            download_from_spotify(url, screen, directory=screen.directory)
        else:
            download_from_spotify(url, screen)
    else:
        screen.append_text(url + ' Not Spotify or YouTube link')


if __name__ == '__main__':
    screen = Screen()
    screen.download_btn.configure(command=lambda: Thread(target=downloading_process).start())
    screen.folder_btn.configure(command=screen.select_folder)
    screen.clear_console_btn.configure(command=screen.clear_console)
    screen.screen_show()