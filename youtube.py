import os
import platform
import time
from threading import Thread

import youtube_dl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import artwork
import metadata
import spotify
import utils


def download_from_yt(url, screen, directory=None):
    if 'playlist' in url:
        screen.append_text('Playlist Found\n')
        Thread(target=download_playlist, args=(url, screen, directory,)).start()
    else:

        music_title, artist = extract_single_title(url)
        if music_title:
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
    downloaded_path = download(url, screen, directory, music_title, artist)
    handle_metadata(downloaded_path, music_title, artist)
    screen.set_downloadbtn_normal()


def find_info_from_spotify(track, artist):
    if not track or not artist:
        return
    url = 'https://open.spotify.com/search/' + track + '%20' + artist
    # r = requests.get(url)
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")

    if platform.system() == 'Windows':
        driver = webdriver.Chrome('Driver/Windows/chromedriver.exe', options=chrome_options)
    else:
        driver = webdriver.Chrome('Driver/MacOs/chromedriver', options=chrome_options)
    driver.get(url)

    soup = BeautifulSoup(driver.page_source.encode("utf-8"), 'html.parser')
    driver.quit()

    track_link = None
    sections = soup.find_all(attrs='react-contextmenu-wrapper')
    for section in sections:
        href = section.find_next('a')['href']
        base_spotify = 'https://open.spotify.com'
        link = base_spotify + href
        if 'track' in link:
            track_link = link
            break
    if track_link:
        print(track_link)
        music = spotify.selenium_parse(track_link)
        return music


def handle_metadata(downloaded_path, track_title, artist):
    info = find_info_from_spotify(track_title, artist)
    if not info:
        return
    music_tags = {
        'track_name': info['track_name'],
        'artist': info['artist'],
        'album': info['album'],
        'genre': '',
    }
    metadata.paste_tags(downloaded_path, music_tags)
    artwork.download_artwork(info['cover_link'])

    if os.path.exists(utils.downloaded_image_path):
        artwork.embed_in_songfile(downloaded_path, utils.downloaded_image_path)
        os.remove(utils.downloaded_image_path)


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
        # Download
        downloaded_path = download(url, screen, directory, track_title, artist)
        # Metadata
        handle_metadata(downloaded_path, track_title, artist)

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
    # Add Information
    if music_title and artist:
        screen.append_text('music title:' + music_title + '\n')
        screen.append_text('artist:' + artist + '\n')
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:

            # Download
            screen.append_text('downloading\n')
            screen.append_text('|')
            ydl.download([url])
    except:
        screen.append_text('Error occured when downloading or converting\n')
        return

    global path
    if path.endswith('webm'):
        path = path.replace('webm', 'mp3')
    else:
        path = path.replace('m4a', 'mp3')
    return path
