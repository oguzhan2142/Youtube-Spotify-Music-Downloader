import unittest

from metadata import Metadata
from screen import Screen
from spotify import selenium_parse


class TestStringMethods(unittest.TestCase):

    def test_album_tags(self):
        urls = [
            'https://open.spotify.com/album/6fDShEba0e8Z5JRkOOmi7r',
            'https://open.spotify.com/album/3lSeFRXenFqW9zm8tEKCxx',
            'https://open.spotify.com/album/1vaHaExD4RbTtZcQpiqix1',
        ]

        screen = Screen()
        for url in urls:
            musics = selenium_parse(url, screen)
            for music in musics:
                m = Metadata()
                m.search_tags(music['track_name'], music['artist'])
                self.assertNotEqual(m.label, '', msg='label:' + m.label)
                self.assertNotEqual(m.album, '', msg='album:' + m.album)


if __name__ == '__main__':
    unittest.main()
