import unittest

from metadata import Metadata
from screen import Screen
from spotify import selenium_parse
import utils

class MetadataTest(unittest.TestCase):
    def test_search_tags(self):
        album_urls = [
            # 'https://open.spotify.com/album/6fDShEba0e8Z5JRkOOmi7r',
            # 'https://open.spotify.com/album/3lSeFRXenFqW9zm8tEKCxx',
            # 'https://open.spotify.com/album/1vaHaExD4RbTtZcQpiqix1',
        ]

        playlist_urls = [
            'https://open.spotify.com/playlist/3U32XSo45tggnTAhXuYPSD',
        ]

        single_urls=[
            'https://open.spotify.com/track/19To9JYwjSWCKlDCZj1N0P',
            'https://open.spotify.com/track/5NQMadp0xeaIslLlzJZ80m',
        ]

        self.search_tags(single_urls)

    def search_tags(self, urls):
        screen = Screen()
        for url in urls:
            print(url, ':')
            musics = selenium_parse(url, screen)
            for music in musics:
                print('*' * 20)
                print(music['track_name'], '-', music['artist'])
                m = Metadata()
                m.search_tags(music['track_name'], music['artist'])
                print('album:', m.album)
                self.assertNotEqual(m.label, '', msg='label:' + m.label)
                self.assertNotEqual(m.album, '', msg='album:' + m.album)
        utils.remove_img()


if __name__ == '__main__':
    unittest.main()
