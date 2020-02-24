import youtube_dl


def download_from_yt():
    pass


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
