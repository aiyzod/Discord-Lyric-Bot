from io import StringIO
from requests import get
from bs4 import BeautifulSoup as bs


class lyric:
    title = ''
    artist = ''
    img = ''
    lyric = ''

    def __init__(self, keyword) -> None:
        self.keyword = keyword
        self.find()

    def find(self):
        r = get(f'https://www.kkbox.com/api/search/song?q={self.keyword}&terr=tw&lang=tc')
        res = r.json()['data']['result']

        if res:
            r = get(res[0]['url'])
            self.lyric = bs(r.text, 'html.parser').select_one('div.lyrics').get_text()

            if '暫無歌詞' in self.lyric:
                self.lyric = '暫無歌詞'
            else:
                self.lyric = ''.join([line if line.strip(' ') in ['\r\n', '\n'] else line.lstrip() for line in StringIO(self.lyric)])

        self.title = bs(r.text, 'html.parser').select_one('div.title h1').get_text()
        self.img = bs(r.text, 'html.parser').select_one('div.image-container img').get('src')
        self.artist = bs(r.text, 'html.parser').select_one('div.artist a')

        if self.artist is None:
            self.artist = bs(r.text, 'html.parser').select_one('div.artist').get_text()
        else:
            self.artist = self.artist.get('title')