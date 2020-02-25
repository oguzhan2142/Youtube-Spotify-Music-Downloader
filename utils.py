downloads_finished = 'All Downloads Finished Successfully'


def wait_threads_loop(threads):
    while len(threads) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
