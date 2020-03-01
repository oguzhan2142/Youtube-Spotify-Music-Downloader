from threading import Thread
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch
from youtube import download_single_mp3
from utils import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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

    return {
        'artist': artist,
        'track_name': track_name,
        'duration': give_float_value(duration),
    }


def selenium_parse(url):
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
        print('artist page')
        return parse_artist(soup)
    elif 'album' in url:
        print('album page')
        return parse_album_or_playlist(soup)
    elif 'playlist' in url:
        print('playlist page')
        return parse_album_or_playlist(soup)
    else:
        print('track page')
        return parse_track(soup)


def search_videos_on_youtube(music):
    matched_result = None
    query = music['artist'] + ' ' + music['track_name']
    found_videos = YoutubeSearch(query, max_results=10)
    videos = found_videos.videos

    if found_videos:
        for video in videos:
            track_name = get_plain_string(music['track_name'].lower())
            video_name = get_plain_string(video['title'].lower())
            if track_name in video_name:
                matched_result = video
                break

    return matched_result


def download_from_spotify(url, screen, directory=None):
    youtube_url = 'https://www.youtube.com'
    playlist = selenium_parse(url)
    downloaded_counter = 0
    threads = []
    skipped_musics = []
    screen.append_text(str(len(playlist)) + ' music found\n')
    for music in playlist:
        # Video Arama
        matched_result = search_videos_on_youtube(music)

        if not matched_result:
            skipped_musics.append(music['track_name'])
            continue

        # Indirme
        first_yt_link = matched_result['link']
        screen.append_text(music_header + music['track_name'] + downloading + '\n')
        download_link = youtube_url + first_yt_link
        thread = Thread(target=download_single_mp3, args=(download_link, screen, directory, music['track_name'],))
        downloaded_counter += 1
        threads.append(thread)
        thread.start()

    wait_threads_loop(threads)
    screen.append_text(all_downloads_finished)

    screen.append_text(summary)
    screen.append_text(str(downloaded_counter) + ' music downloaded\n')

    if screen.directory:
        screen.append_text('Downloaded Folder:' + screen.directory + '\n')
    else:
        screen.append_text('Downloaded Folder:' + give_desktop_path() + '\n')

    if skipped_musics:
        screen.append_text(str(len(skipped_musics)) + ' music couldn\'t download:\n')
        for index, skipped_music in enumerate(skipped_musics):
            screen.append_text('\t' + str(index + 1) + skipped_music + '\n')
