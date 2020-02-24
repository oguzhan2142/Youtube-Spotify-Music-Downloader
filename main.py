from screen import Screen
from spotify import *
from youtube import *


def downloading_process():
    #   https://open.spotify.com/playlist/7IImK40Rng4pclYflKPLs9
    #   https://www.youtube.com/watch?v=rr0gvSS1OzE&t=1024s
    url = screen.E1.get()
    if url:
        screen.append_text('Downloads Starting...\n')
    else:
        screen.append_text('Can\'t find a url\n')
        return

    if 'youtube' in url:
        # youtube
        screen.append_text('Downloading from YouTube\n')
        download_from_yt(url, screen)
    else:
        # spotify
        screen.append_text('Downloading from Spotify\n')
        download_from_spotify(url, screen)


if __name__ == '__main__':
    screen = Screen()
    screen.status.set('Waiting For Link')

    screen.B.configure(command=lambda: Thread(target=downloading_process).start())
    screen.screen_show()
