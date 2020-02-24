import youtube_dl
from threading import Thread


def download_from_yt(url, screen):
    if 'playlist' in url:
        screen.append_text('Playlist Found\n')
        Thread(target=download_playlist, args=(url, screen,)).start()
    else:
        Thread(target=download_single_mp3, args=(url, screen,)).start()


def extract_playlist(playlist_url):
    ydl = youtube_dl.YoutubeDL({'dump_single_json': True,
                                'extract_flat': True})
    with ydl:
        dic = ydl.extract_info(playlist_url, False)
    return dic['entries']


def download_playlist(playlist_url, screen):
    base_url = 'https://www.youtube.com/watch?v='
    playlist = extract_playlist(playlist_url)
    for music in playlist:
        url = base_url + music['url']
        screen.append_text(music['title'] + ' downloading\n')
        Thread(target=download_single_mp3, args=(url, screen, music['title'])).start()


def download_single_mp3(url, screen, music_title=None):
    def my_hook(d):
        if d['status'] == 'error':
            screen.append_text('error occured\n')
        if d['status'] == 'finished':
            if music_title:
                screen.append_text(music_title + ' Downloaded\n')
                screen.append_text(music_title + ' Converting to mp3...\n')
            else:
                screen.append_text(d['filename'] + ' downloaded.Converting to mp3...\n')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
        'noplaylist': True,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        if music_title:
            screen.append_text(music_title + ' converted mp3 succesfully\n')
        else:
            screen.append_text('File converted mp3 succesfully\n')