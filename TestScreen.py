from mpd import MPDClient
from AbstractScreen import AbstractScreen
from ScrollingStrategy import ScrollingStrategy
from SongInfo import SongInfo

__author__ = 'diego'

class TestScreen(AbstractScreen):

    #_newContent = "Pink Floyd - The Wall - Another Brick In The Wall Part II"
    #_newContent = "Pink Floyd - The Wall"
    client = MPDClient()
    client.timeout = 10                # network timeout in seconds (floats allowed), default: None
    client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
    client.connect("192.168.178.42", 6600)  # connect to localhost:6600
    print(client.mpd_version)          # print the MPD version
    #_si = SongInfo({'album': 'The Dark Side Of The Moon (24 bits/96kHz)', 'date': '1973', 'title': 'On The Run', 'track': '03', 'artist': 'Pink Floyd', 'pos': '3', 'last-modified': '2012-06-02T19:36:08Z', 'albumartist': ['Pink Floyd', 'Pink Floyd'], 'file': 'NAS/Diskstation/flac/Pink Floyd/Pink Floyd - Dark Side of The Moon (24-96)/03 - On The Run.flac', 'time': '226', 'genre': 'Progressive Rock', 'id': '3'})
    #_si = SongInfo({'id': '0', 'pos': '0', 'name': 'TheJazzGroove.com - Laid-back Jazz', 'file': 'http://199.180.72.2:8015', 'title': 'Eddie Higgins Quartet (feat. Scott Hamilton) - Melancholy Rhapsody'})
    _si = SongInfo(client.currentsong())
    _newContent = str(_si)
    _scrollingStrategy = None

    def __init__(self,content, aDisplay):
        super(TestScreen,self).__init__(content, aDisplay)
        self._scrollingStrategy = ScrollingStrategy(aDisplay, 2, 16, 40)

    def update_content(self):
        self._scrollingStrategy.update_display(self._newContent)

    def execute_command_UP(self):
        self._newContent = "Diego"
        self.set_backlight_colour_to_red()
        return self

    def execute_command_DOWN(self):
        self._newContent = "Giovanna"
        self.set_backlight_colour_to_green()
        return self

    def execute_command_LEFT(self):
        self._newContent = "Valerio"
        self.set_backlight_colour_to_yellow()
        return self

    def execute_command_RIGHT(self):
        self._newContent = "Claudio"
        self.set_backlight_colour_to_blue()
        return self

    def execute_command_SELECT(self):
        self._newContent = "Giulia"
        self.set_backlight_colour_to_violet()
        return self

    def execute_command_LEFT_AND_RIGHT(self):
        self._newContent = "Valerio e Claudio"
        self.set_backlight_colour_to_teal()
        return self

    def execute_command_UP_AND_DOWN(self):
        self._newContent = "Giovanna e Diego"
        self.set_backlight_colour_to_white()
        return self

