import platform
import os

all_downloads_finished = 'All Downloads Finished Successfully\n'
downloading = '\ndownloading:       [######              ]'
converting = '\nconverting:        [############        ]'
converted = '\nconverted to mp3:  [####################]'
music_header = '--->'


def wait_threads_loop(threads):
    while len(threads) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)


def give_desktop_path():
    music_template = '/%(title)s.%(ext)s'

    if platform.system() == 'Windows':
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Downloads/')
    else:
        userhome = os.path.expanduser('~')
        desktop_path = userhome + '/Desktop/Downloads/'

    download_directory = desktop_path + music_template
    return download_directory


def give_float_value(string):
    array = string.split(':')
    new_string = ''
    new_string += array[0]
    new_string += '.'
    new_string += array[1]
    return float(new_string)
