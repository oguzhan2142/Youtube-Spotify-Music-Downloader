from difflib import SequenceMatcher

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import *
from youtube import download
from youtube import extract_playlist_info


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
            'duration': give_float_value(duration_in_row),
        })

    return playlist


def get_similar_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()


def parse_album_or_playlist(soup):
    playlist = []
    all_rows = soup.find_all(attrs={'class': 'tracklist-row'})
    for row in all_rows:
        artist_in_row = row.find(attrs={'class': 'tracklist-row__artist-name-link'}).text
        trackname_in_row = row.find(attrs={'class': 'tracklist-name ellipsis-one-line'}).text
        duration_in_row = row.find(attrs={'class': 'tracklist-duration'}).text
        playlist.append({
            'artist': artist_in_row,
            'track_name': trackname_in_row,
            'duration': give_float_value(duration_in_row),
        })

    return playlist


def parse_track(soup):
    title = soup.find(attrs={'property': 'og:title'})
    track_name = title.get('content')

    all_rows = soup.find_all(attrs={'class': 'tracklist-row'})
    track_row = None
    for row in all_rows:
        trackname_in_row = row.find(attrs={'class': 'tracklist-name ellipsis-one-line'}).text
        if track_name == trackname_in_row:
            track_row = row
            break

    artist = track_row.find(attrs={'class': 'second-line'}).text
    duration = track_row.find(attrs={'class': 'tracklist-duration'}).text

    return [{
        'artist': artist,
        'track_name': track_name,
        'duration': give_float_value(duration),
    }]


def selenium_parse(url, screen):
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
        screen.append_text('Artist Page Found\n')
        return parse_artist(soup)
    elif 'album' in url:
        screen.append_text('Album Page Found\n')
        return parse_album_or_playlist(soup)
    elif 'playlist' in url:
        screen.append_text('Playlist Page Found\n')
        return parse_album_or_playlist(soup)
    else:
        screen.append_text('Track Page Found\n')
        return parse_track(soup)


def find_highest_related_video(music, duration_in_spotify):
    static_duration = 3.0
    query = music['artist'] + ' ' + music['track_name']
    music_name = get_plain_string(music['track_name']).lower()
    query = 'https://www.youtube.com/results?search_query=' + string_to_querystring(query)
    videos = extract_playlist_info(query)
    high_ratio = 0
    video_ratio = {}
    for video in videos:
        video_name = get_plain_string(video['title']).lower()
        duration_in_spotify = float(duration_in_spotify)
        if duration_in_spotify > static_duration + 1.5 or duration_in_spotify < static_duration - 1.5:
            continue

        ratio = get_similar_ratio(music_name, video_name)
        video_ratio[ratio] = video
        if ratio > high_ratio:
            high_ratio = ratio
    print('high ratio', high_ratio)
    return video_ratio[high_ratio]


def download_from_spotify(url, screen, directory=None):
    youtube_base = 'https://www.youtube.com/watch?v='
    playlist = selenium_parse(url, screen)
    downloaded_counter = 0
    skipped_musics = []
    screen.append_text(str(len(playlist)) + ' music found\n')
    for music in playlist:
        # Video Arama
        video = find_highest_related_video(music, music['duration'])
        print(music['track_name'])  # 2.48
        print(music['duration'])
        if not video:
            skipped_musics.append(music['track_name'])
            continue

        # Indirme
        best_url = video['url']
        download_link = youtube_base + best_url
        print('link:', download_link)
        download(download_link, screen, directory, music['track_name'], music['artist'])
        downloaded_counter += 1

    screen.append_text(all_downloads_finished)
    add_summary_to_screen(screen, skipped_musics, downloaded_counter)
    screen.set_downloadbtn_normal()
