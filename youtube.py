import platform
import time
from threading import Thread

import youtube_dl

import utils


def download_from_yt(url, screen, directory=None):
    if 'playlist' or 'list' in url:
        screen.append_text('Playlist Found\n')
        Thread(target=download_playlist, args=(url, screen, directory,)).start()
    else:
        music_title, artist = extract_single_title(url)
        if '(' and ')' in music_title:
            music_title = utils.remove_parantesis(music_title)
        Thread(target=download_single, args=(url, screen, directory, music_title, artist,)).start()


def extract_playlist_info(playlist_url):
    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    ydl = youtube_dl.YoutubeDL({'dump_single_json': True,
                                'extract_flat': True,
                                'forceduration': True,
                                'logger': MyLogger(),
                                })
    with ydl:
        dic = ydl.extract_info(playlist_url, download=False)
    return dic['entries']


def extract_single_title(url):
    ydl = youtube_dl.YoutubeDL({'dump_single_json': True,
                                'extract_flat': True})
    with ydl:
        dic = ydl.extract_info(url, False)
        # return {'track_name': dic['track'], 'artist': dic['artist']}
        return dic['track'], dic['artist']


def download_single(url, screen, directory, music_title, artist):
    download(url, screen, directory, music_title, artist)
    screen.set_downloadbtn_normal()


def find_info_from_spotify(track,artist):
    pass



def download_playlist(playlist_url, screen, directory=None):
    now = int(round(time.time() * 1000))
    base_url = 'https://www.youtube.com/watch?v='
    playlist = extract_playlist_info(playlist_url)
    for music in playlist:
        url = base_url + music['url']
        track_title, artist = extract_single_title(url)
        print(track_title)
        print(artist)
        print()
        # download(url, screen, directory, track_title, artist)
    screen.append_text(utils.all_downloads_finished)
    utils.add_summary_to_screen(screen, downloaded_counter=len(playlist))
    screen.set_downloadbtn_normal()
    last = int(round(time.time() * 1000))
    elapsed_time = (last - now) / 1000
    screen.append_text('elapsed time:' + str(elapsed_time) + ' sec\n')


path = None


def download(url, screen, directory=None, music_title=None, artist=None):
    # now = int(round(time.time() * 1000))
    if directory:
        download_directory = directory + '/%(title)s.%(ext)s'
    else:
        download_directory = utils.give_desktop_path_with_template()

    class MyLogger(object):
        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            print(msg)

    def my_hook(d):
        # d['filename']
        if d['status'] == 'error':
            screen.append_text('error occured when downloading\n' + music_title)
        if d['status'] == 'downloading':
            screen.append_text(d['_percent_str'] + ' |')
        if d['status'] == 'finished':
            global path
            path = d['filename']

    if platform.system() == 'Windows':
        ffmpeg_location = 'ffmpeg/ffmpeg-windows/bin/ffmpeg.exe'
    else:
        ffmpeg_location = 'ffmpeg/ffmpeg-mac/bin/ffmpeg'

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
             'preferredcodec': 'mp3',
             'preferredquality': '192',
             }],

        'ffmpeg_location': ffmpeg_location,
        'outtmpl': download_directory,
        'progress_hooks': [my_hook],
        'noplaylist': True,
        'logger': MyLogger(),
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:

            # Add Information
            screen.append_text('music title:' + music_title + '\n')
            screen.append_text('artist:' + artist + '\n')

            # Download
            screen.append_text('downloading\n')
            screen.append_text('|')
            ydl.download([url])
    except:
        screen.append_text('Error occured when downloading or converting\n')
        return

    # # Edit Metadata
    # screen.append_text('\nMetadata |')
    # print('MUSIC FOR')
    # print('music title', music_title)
    # print('artist', artist)
    global path
    # print('path in download:', path)
    if path.endswith('webm'):
        path = path.replace('webm', 'mp3')
    else:
        path = path.replace('m4a', 'mp3')
    return path
    # print('path in download:', path)
    #
    # is_successful = metadata.create_metadata(path, music_title, artist,album)
    # if is_successful:
    #     screen.append_text(' √ |\n')
    # else:
    #     screen.append_text(' X |\n')

    # last = int(round(time.time() * 1000))
    # elapsed_time = (last - now) / 1000
    # screen.append_text('total elapsed time:' + str(elapsed_time) + ' sec\n\n')
