import os
import platform

all_downloads_finished = '\nProgress Finished Successfully\n'
downloaded_image_path = 'img.png'


def remove_img():
    if os.path.exists(downloaded_image_path):
        # Remove Downloaded Image if exist
        os.remove(downloaded_image_path)


def remove_parantesis(string_parantesis):
    start_index = string_parantesis.index('(')
    end_index = string_parantesis.index(')')

    string_without_parantesis = string_parantesis[:start_index] + string_parantesis[end_index + 1:]
    return strip_text(string_without_parantesis)


def add_summary_to_screen(screen, skipped_musics=None, downloaded_counter=None):
    screen.append_text('\n*********************Summary*********************\n')
    if downloaded_counter:
        screen.append_text(str(downloaded_counter) + ' music downloaded\n')

    if screen.directory:
        screen.append_text('Downloaded Folder:' + screen.directory + '\n')
    else:
        screen.append_text('Downloaded Folder:' + give_desktop_path_with_template() + '\n')

    if skipped_musics:
        screen.append_text(str(len(skipped_musics)) + ' music couldn\'t download:\n')
        for index, skipped_music in enumerate(skipped_musics):
            screen.append_text('  ' + str(index + 1) + ') ' + skipped_music + '\n')
    screen.append_text('\n')


def give_desktop_path():

    if platform.system() == 'Windows':
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\Downloads\\')
    else:
        userhome = os.path.expanduser('~')
        desktop_path = userhome + '/Desktop/Downloads/'
    return desktop_path



def give_desktop_path_with_template():
    music_template = '/%(title)s.%(ext)s'

    if platform.system() == 'Windows':
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop/Downloads/')
    else:
        userhome = os.path.expanduser('~')
        desktop_path = userhome + '/Desktop/Downloads/'

    download_directory = desktop_path + music_template
    return download_directory


def remove_remix(string_with_remix):
    string_with_remix = string_with_remix.lower()
    if 'remix' in string_with_remix:
        string_with_remix = string_with_remix.replace('remix', '')
    return string_with_remix


def remove_noncharacters(string='asd'):
    new_str = ''
    for s in string:
        if 'a' <= s <= 'z':
            new_str += s
    return new_str


def turn_turkishchars_to_englishchars(string='asd'):
    turkish_chars = {
        'ğ': 'g',
        'ı': 'i',
        'ö': 'o',
        'ü': 'u',
        'ş': 's',
        'ç': 'c',
    }
    for key in turkish_chars.keys():
        if key in string:
            string = string.replace(key, turkish_chars[key])
    return string


def extract_cover_link(string):
    start = string.index('//') + 2
    if '")' in string:
        end = string.index('")')
    else:
        end = string.index(')')
    result = 'http://' + string[start:end]

    return result


def give_float_value(string):
    array = string.split(':')
    new_string = ''
    new_string += array[0]
    new_string += '.'
    new_string += array[1]
    return float(new_string)


def string_to_querystring(query_string):
    arr = query_string.split(' ')
    if len(arr) > 1:
        modified = ''
        for index, a in enumerate(arr):
            modified += a
            if index == len(arr) - 1:
                continue
            modified += '+'
        return modified
    else:
        return query_string


def strip_text(string):
    string = string.replace('\n', '')
    string = string.strip()
    return string
