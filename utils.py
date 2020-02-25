all_downloads_finished = 'All Downloads Finished Successfully'
downloading = '\ndownloading:       [######              ]'
converting = '\nconverting:        [############        ]'
converted = '\nconverted to mp3:  [####################]'
music_header = '--->'


def wait_threads_loop(threads):
    while len(threads) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
