import platform
from threading import Thread

import youtube_dl
from mutagen.easyid3 import error

import metadata
import utils


def download_from_yt(url, screen, directory=None):
    if 'playlist' in url:
        screen.append_text('Playlist Found\n')
        Thread(target=download_playlist, args=(url, screen, directory,)).start()
    else:
        title = extract_single_title(url)
        Thread(target=download_single_mp3, args=(url, screen, directory, title,)).start()


def extract_playlist_info(playlist_url):
    ydl = youtube_dl.YoutubeDL({'dump_single_json': True,
                                'extract_flat': True})
    with ydl:
        dic = ydl.extract_info(playlist_url, False)
    return dic['entries']


def extract_single_title(url):
    ydl = youtube_dl.YoutubeDL({'dump_single_json': True,
                                'extract_flat': True})
    with ydl:
        dic = ydl.extract_info(url, False)
        return dic['track']


def download_playlist(playlist_url, screen, directory=None):
    base_url = 'https://www.youtube.com/watch?v='
    playlist = extract_playlist_info(playlist_url)
    for music in playlist:
        url = base_url + music['url']
        download_single_mp3(url, screen, directory, music['title'])
    screen.append_text(utils.all_downloads_finished)
    utils.add_summary_to_screen(screen, downloaded_counter=len(playlist))


def download_single_mp3(url, screen, directory=None, music_title=None, artist=None):
    def my_hook(d):
        if d['status'] == 'error':
            screen.append_text('error occured when downloading\n' + music_title)
        if d['status'] == 'downloading':
            screen.append_text(d['_percent_str'])

        # if d['status'] == 'finished':

    if directory:
        download_directory = directory + '/%(title)s.%(ext)s'
    else:
        download_directory = utils.give_desktop_path_with_template()

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

            # Add Information
            screen.append_text(utils.music_header + music_title + ':\n')

            # Download
            screen.append_text('downloading\n')
            ydl.download([url])
    except:
        screen.append_text('Error occured when downloading or converting\n')
        return
    try:
        # Edit Metadata
        screen.append_text('\nediting metadata\n')
        if artist:
            metadata.create_metadata(screen.directory, music_title, artist)
        else:
            metadata.create_metadata(screen.directory, music_title=music_title)
        screen.append_text('metadata added\n')
    except error:
        screen.append_text('Error occured when editing metadata\n')
