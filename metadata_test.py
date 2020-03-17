import unittest

import utils
from metadata import Metadata
from screen import Screen
from spotify import selenium_parse


class MetadataTest(unittest.TestCase):
    # Album
    def initilized_links(self):
        self.album_urls = [
            'https://open.spotify.com/album/6fDShEba0e8Z5JRkOOmi7r',
            'https://open.spotify.com/album/3lSeFRXenFqW9zm8tEKCxx',
            'https://open.spotify.com/album/1vaHaExD4RbTtZcQpiqix1',
            'https://open.spotify.com/album/3nzuGtN3nXARvvecier4K0',
            'https://open.spotify.com/album/1yjH4I5n73eBy1v2pWuL22',
            'https://open.spotify.com/album/662MMKEWOxGXbPXQIcgBlW',
            'https://open.spotify.com/album/3nzuGtN3nXARvvecier4K0',
            'https://open.spotify.com/album/1US66auJ538TiXGeUf24yL',
        ]
        # Sanatci
        self.artist_urls = [
            'https://open.spotify.com/artist/7vk5e3vY1uw9plTHJAMwjN',
            'https://open.spotify.com/artist/64KEffDW9EtZ1y2vBYgq8T',
            'https://open.spotify.com/artist/5q0uL3T6JoEVGylrtCnfCb',
            'https://open.spotify.com/artist/1tgfi3YYoeXKehnjKaMsOo',
            'https://open.spotify.com/artist/64KEffDW9EtZ1y2vBYgq8T',
            'https://open.spotify.com/artist/4ckLjJztj53Ifid7WHweBn',
        ]
        # Calma listesi
        self.playlist_urls = [
            'https://open.spotify.com/playlist/3U32XSo45tggnTAhXuYPSD',
            'https://open.spotify.com/playlist/37i9dQZF1DX29mEFPXNhRM',
            'https://open.spotify.com/playlist/3SoZlNAFp6tALFmCLRyO09',
            'https://open.spotify.com/playlist/37i9dQZF1DX9ASuQophyb3',
            'https://open.spotify.com/playlist/37i9dQZF1DWX83CujKHHOn',
        ]
        # Tekli Sarki
        self.track_urls = [
            'https://open.spotify.com/track/19To9JYwjSWCKlDCZj1N0P',
            'https://open.spotify.com/track/5NQMadp0xeaIslLlzJZ80m',
            'https://open.spotify.com/track/08bNPGLD8AhKpnnERrAc6G',
            'https://open.spotify.com/track/7nWMcuT0Ao3rH3hsLNv4Ob',
            'https://open.spotify.com/track/1RqNAiL2toZ59HTjQbFLfM',
            'https://open.spotify.com/track/4dOTkX5E9MqGArY8yMaM6X',
            'https://open.spotify.com/track/6vbgHYlDD0fwSU54D2bD6o',
            'https://open.spotify.com/track/0FNgddJJSTS9gSS8QGcxG2',
        ]

    def test_search_tags(self):
        pass

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

    def test_same_album(self):
        self.initilized_links()
        screen = Screen()
        musics = selenium_parse(self.album_urls[1], screen)
        m = Metadata()
        m.search_tags(musics[0]['track_name'], musics[0]['artist'])
        first_ones_album = m.album

        for music in musics:
            print('\n')
            print(music['track_name'], '---', music['artist'])
            m.search_tags(music['track_name'], music['artist'])
            msg = 'first one album:' + first_ones_album
            self.assertEqual(first_ones_album, m.album, msg=msg)
        utils.remove_img()


if __name__ == '__main__':
    unittest.main()
