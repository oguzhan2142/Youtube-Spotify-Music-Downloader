import os
import platform
import time
from difflib import SequenceMatcher

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import artwork
import metadata
import utils
from youtube import download
from youtube import extract_playlist_info


# IPTAL
def parse_artist(soup):
    artist = soup.find(attrs={'class': 'large'})
    artist = artist.text
    playlist = []
    all_rows = soup.find_all(attrs={'class': 'tracklist-row'})

    for row in all_rows:
        trackname_in_row = row.find(attrs={'class': 'tracklist-name ellipsis-one-line'}).text
        duration_in_row = row.find(attrs={'class': 'tracklist-duration'}).text
        playlist.append({
            'artist': artist,
            'track_name': trackname_in_row,
            'duration': utils.give_float_value(duration_in_row),
        })

    return playlist


def get_similar_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()


def parse_playlist(soup):
    playlist = []
    spotify_url = 'https://open.spotify.com'

    all_rows = soup.find_all(attrs={'class': 'tracklist-row'})
    for row in all_rows:
        artist_in_row = row.find(attrs={'class': 'tracklist-row__artist-name-link'}).text
        trackname_in_row = row.find(attrs={'class': 'tracklist-name ellipsis-one-line'}).text
        duration_in_row = row.find(attrs={'class': 'tracklist-duration'}).text
        album_in_row = row.find(attrs={'class': 'tracklist-row__album-name-link'}).text
        href = row.find(attrs={'class': 'tracklist-row__album-name-link'})['href']
        album_link = spotify_url + href
        r = requests.get(album_link)
        album_soup = BeautifulSoup(r.content, 'html.parser')
        link = album_soup.find(attrs={'class': 'cover-art-image'})
        cover_link = utils.extract_cover_link(link['style'])
        playlist.append({
            'artist': artist_in_row,
            'album': album_in_row,
            'track_name': trackname_in_row,
            'duration': utils.give_float_value(duration_in_row),
            'cover_link': cover_link,
        })

    return playlist


def parse_album(soup):
    playlist = []
    all_rows = soup.find_all(attrs={'class': 'tracklist-row'})
    div_album = soup.find('div', attrs={'class': 'TrackListHeader__entity-name'})
    span_album = div_album.find_next('span', attrs={'dir': 'auto'})
    album = span_album.text

    cover_link = soup.find(attrs={'class': 'cover-art-image'})
    print(cover_link['style'])
    link = utils.extract_cover_link(cover_link['style'])
    print(link)

    for row in all_rows:
        artist_in_row = row.find(attrs={'class': 'tracklist-row__artist-name-link'}).text
        trackname_in_row = row.find(attrs={'class': 'tracklist-name ellipsis-one-line'}).text
        duration_in_row = row.find(attrs={'class': 'tracklist-duration'}).text
        playlist.append({
            'artist': artist_in_row,
            'album': album,
            'track_name': trackname_in_row,
            'duration': utils.give_float_value(duration_in_row),
            'cover_link': link,
        })

    return playlist


def parse_track(soup):
    title = soup.find(attrs={'property': 'og:title'})
    track_name = title.get('content')

    div_album = soup.find('div', attrs={'class': 'TrackListHeader__entity-name'})
    span_album = div_album.find_next('span', attrs={'dir': 'auto'})
    album = span_album.text

    cover_link = soup.find(attrs={'class': 'cover-art-image'})
    link = utils.extract_cover_link(cover_link['style'])

    all_rows = soup.find_all(attrs={'class': 'tracklist-row'})
    track_row = None
    for row in all_rows:
        trackname_in_row = row.find(attrs={'class': 'tracklist-name ellipsis-one-line'}).text
        if track_name == trackname_in_row:
            track_row = row
            break

    artist = track_row.find(attrs={'class': 'second-line'}).text
    duration = track_row.find(attrs={'class': 'tracklist-duration'}).text
    return {
        'artist': artist,
        'album': album,
        'track_name': track_name,
        'duration': utils.give_float_value(duration),
        'cover_link': link,
    }


def selenium_parse(url, screen=None):
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

    if 'artist' in url:
        if screen:
            screen.append_text('Artist Page Found\n')
            screen.append_text('Artist Page Part Broken\n')
        # return parse_artist(soup)
    elif 'album' in url:
        if screen:
            screen.append_text('Album Page Found\n')
        return parse_album(soup)
    elif 'playlist' in url:
        if screen:
            screen.append_text('Playlist Page Found\n')
        return parse_playlist(soup)
    else:
        if screen:
            screen.append_text('Track Page Found\n')
        return parse_track(soup)


def find_highest_related_video(music):
    static_duration = 3.0
    music_name = music['track_name'].lower()
    artist = music['artist'].lower()
    artist_track = music_name + ' ' + artist
    search_link = 'https://www.youtube.com/results?search_query=' + utils.string_to_querystring(artist_track)
    videos = extract_playlist_info(search_link)

    for video in videos:
        # bazilarinda title yok
        if 'title' not in video:
            continue

        video_name = video['title'].lower()
        duration_in_spotify = float(music['duration'])

        if duration_in_spotify > static_duration + 2.5 or duration_in_spotify < static_duration - 2.0:
            continue

        if artist in video_name and music_name in video_name:
            return video

    return videos[0]


def download_from_spotify(url, screen, directory=None):
    now = int(round(time.time() * 1000))
    youtube_base = 'https://www.youtube.com/watch?v='
    playlist = selenium_parse(url, screen)
    downloaded_counter = 0
    skipped_musics = []
    screen.append_text(str(len(playlist)) + ' music found\n')
    for index, music in enumerate(playlist, start=1):
        # Video Arama

        video = find_highest_related_video(music)

        if not video:
            skipped_musics.append(music['track_name'])
            continue

        # Download
        best_url = video['url']
        download_link = youtube_base + best_url
        screen.append_text('\n' + str(index) + ' / ' + str(len(playlist)) + '\n')
        downloaded_path = download(download_link, screen, directory, music['track_name'], music['artist'])
        print('path:', downloaded_path)
        downloaded_counter += 1

        # Metadata
        music_tags = {
            'track_name': music['track_name'],
            'artist': music['artist'],
            'album': music['album'],
            'genre': '',
        }

        metadata.paste_tags(downloaded_path, music_tags)
        artwork.download_artwork(music['cover_link'])

        if os.path.exists(utils.downloaded_image_path):
            artwork.embed_in_songfile(downloaded_path, utils.downloaded_image_path)
            os.remove(utils.downloaded_image_path)

    last = int(round(time.time() * 1000))
    elapsed_time = (last - now) / 1000
    screen.append_text(utils.all_downloads_finished)
    utils.add_summary_to_screen(screen, skipped_musics, downloaded_counter)
    screen.append_text('total elapsed time:' + str(elapsed_time) + ' sec\n')
    screen.set_downloadbtn_normal()
