import youtube_dl
from threading import Thread


def download_from_yt(url, screen):
    if 'playlist' in url:
        screen.append_text('playlist found\n')
        Thread(target=extract_playlist_info, args=(url, screen,)).start()
    else:
        print('tekli')
        # download_mp3(url, screen)


def download_playlist(playlist_url, screen):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s',
        # 'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        infos = ydl.extract_info(playlist_url, download=False)
        archive = ydl.record_download_archive()
        screen.append_text(infos[0]['title'])
        screen.append_text(infos[1]['title'])
        # title
        # webpage_url

        print(infos.keys())
        # ydl.download([playlist_url])


def extract_playlist_info(playlist_url, screen):
    ydl = youtube_dl.YoutubeDL({'dump_single_json': True,
                                'extract_flat': True})

    with ydl:
        # results = ydl.download([playlist_url])
        dic = ydl.extract_info(playlist_url,False)

    print(type(dic))
    for result in dic:
        print(result)

    print(dic['webpage_url'])
    print(dic['title'])
    print(dic['entries'])
def download_mp3(url, screen):
    def my_hook(d):
        if d['status'] == 'error':
            screen.append_text('error occured\n')
        if d['status'] == 'finished':
            screen.append_text(d['filename'] + ' finished...\n')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'Downloads/%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
