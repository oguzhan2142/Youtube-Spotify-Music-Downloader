import youtube_dl
from threading import Thread
from utils import *
import platform


def download_from_yt(url, screen, directory=None):
    if 'playlist' in url:
        screen.append_text('Playlist Found\n')
        Thread(target=download_playlist, args=(url, screen, directory,)).start()
    else:
        Thread(target=download_single_mp3, args=(url, screen, directory,)).start()


def extract_playlist(playlist_url):
    ydl = youtube_dl.YoutubeDL({'dump_single_json': True,
                                'extract_flat': True})
    with ydl:
        dic = ydl.extract_info(playlist_url, False)
    return dic['entries']


def download_playlist(playlist_url, screen, directory=None):
    base_url = 'https://www.youtube.com/watch?v='
    playlist = extract_playlist(playlist_url)
    threads = []
    for music in playlist:
        url = base_url + music['url']
        screen.append_text(music_header + music['title'] + downloading + '\n')
        thread = Thread(target=download_single_mp3, args=(url, screen, directory, music['title'],))
        threads.append(thread)
        thread.start()
    wait_threads_loop(threads)
    screen.append_text(all_downloads_finished)


def download_single_mp3(url, screen, directory=None, music_title=None):
    def my_hook(d):
        if d['status'] == 'error':
            screen.append_text('error occured when downloading\n' + music_title)
        if d['status'] == 'finished':
            if music_title:
                screen.append_text(music_header + music_title + converting + '\n')
            else:
                screen.append_text(music_header + d['filename'] + converting + '\n')

    download_directory = '../Downloads/%(title)s.%(ext)s'
    if directory:
        download_directory = directory + '/%(title)s.%(ext)s'

    if platform.system() == 'Windows':
        ffmpeg_location = 'ffmpeg/ffmpeg-windows/bin/ffmpeg.exe'
    else:
        ffmpeg_location = 'ffmpeg/ffmpeg-mac/bin/ffmpeg'

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],

        'ffmpeg_location': ffmpeg_location,
        'outtmpl': download_directory,
        'progress_hooks': [my_hook],
        'noplaylist': True,
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            if music_title:
                screen.append_text(music_header + music_title + converted + '\n')
            else:
                screen.append_text(music_header + 'File' + converted + '\n')
    except:
        screen.append_text(music_title + ' Error Occured\n')
