from mutagen.easyid3 import EasyID3


def paste_tags(path, tags):
    audio = EasyID3(path)
    audio["title"] = tags['track_name']
    audio['album'] = tags['album']
    audio['artist'] = tags['artist']
    audio["genre"] = tags['genre']
    # audio["releasecountry"] = self.country
    # audio["date"] = utils.extract_date(self.realese_date)
    audio.save()
