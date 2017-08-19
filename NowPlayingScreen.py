# volumio-lcd-screen: shows relevant mpd infos on Adafruit 16x2 LCD Plate
# Copyright (C) 2014  Diego Novelli <dnovelli@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
from mpd import MPDClient
from AbstractScreen import AbstractScreen
from SongInfo import SongInfo
from PlayerInfo import PlayerInfo
from ScrollingStrategy import ScrollingStrategy
from TransientScreenDecorator import TransientScreenDecorator

__author__ = 'diego'

class NowPlayingScreen(AbstractScreen):
    '''
    This class represents the most important screen, the one which shows the "now playing" informations.
    Any time a new song starts, it scrolls on the first line artist, album and title.
    When the scroll is over, on the first line there's the title, on the second an icon representing the player status,
    the elapsed time of the song and the player volume.

    This screen uses the python-mpd2 library as client to the MPD
    '''

    # Custom characters
    # play
    ICON_PLAY = [0b01000,
                 0b01100,
                 0b01110,
                 0b01111,
                 0b01110,
                 0b01100,
                 0b01000,
                 0b00000]
    # stop
    ICON_STOP =  [0b00000,
                  0b11111,
                  0b11111,
                  0b11111,
                  0b11111,
                  0b11111,
                  0b00000,
                  0b00000]
    # pause
    ICON_PAUSE = [0b11011,
                  0b11011,
                  0b11011,
                  0b11011,
                  0b11011,
                  0b11011,
                  0b11011,
                  0b00000]
    # vol icons
    ICON_VOL_1 = [0b00001,
                  0b00011,
                  0b01111,
                  0b01111,
                  0b01111,
                  0b00011,
                  0b00001,
                  0b00000]

    ICON_VOL_2 = [0b01000,
                  0b10000,
                  0b00000,
                  0b11000,
                  0b00000,
                  0b10000,
                  0b01000,
                  0b00000]

    # Custom characters address on LCD RAM
    PLAY_ADDRESS = 0x01
    STOP_ADDRESS = 0x02
    PAUSE_ADDRESS = 0x03
    VOL_1_ADDRESS = 0x04
    VOL_2_ADDRESS = 0x05

    # Dictionary to link RAM addresses and custom character bitmasks
    _icon_dict = {int(PLAY_ADDRESS):ICON_PLAY,
                  int(STOP_ADDRESS):ICON_STOP,
                  int(PAUSE_ADDRESS):ICON_PAUSE,
                  int(VOL_1_ADDRESS):ICON_VOL_1,
                  int(VOL_2_ADDRESS):ICON_VOL_2}

    # Dictionary to link MPD status to icons RAM addresses

    _player_info_state_to_icon_addr_dict = {PlayerInfo.PLAY:chr(PLAY_ADDRESS),
                                              PlayerInfo.STOP:chr(STOP_ADDRESS),
                                              PlayerInfo.PAUSE:chr(PAUSE_ADDRESS)}

    def __init__(self, content, aDisplay):
        super(NowPlayingScreen,self).__init__(content, aDisplay)
        for k in self._icon_dict: # create all custom character on LCD RAM
            self._lcd_display.createChar(k,self._icon_dict[k])
        self._mpd_client = MPDClient()
        self._mpd_client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self._mpd_client.idletimeout = None
        self._current_song = None
        self._current_status = None
        self._scrollingStrategy = None
        #self._mpd_ip_address = "192.168.178.42"
        self._mpd_ip_address = "localhost"
        self._up_and_down_screen = self #Screen to appear when UP and DOWN are pressed together

    @property
    def special_ops_screen(self):
        return self._up_and_down_screen

    @special_ops_screen.setter
    def special_ops_screen(self,a_screen):
        """
        Sets the special operation screen that appears when UP and DOWN keys are pressed together


        :type a_screen: AbstractScreen
        :param a_screen:
        """
        self._up_and_down_screen = a_screen

    def update_content(self):
        self.set_backlight_colour_to_teal()
        self._mpd_client.connect(self._mpd_ip_address, 6600)
        client_status = self._mpd_client.status()
        player_info = PlayerInfo(client_status)
        client_currentsong = self._mpd_client.currentsong()
        if(len(client_currentsong) == 0 and player_info.get_playlist_length() > 0): # added a playlist, but nothing is playing
            client_currentsong = self._mpd_client.playlistid()[0]
        song_info = SongInfo(client_currentsong)
        self._mpd_client.disconnect()
        if(self._current_song != client_currentsong): # Song is changed, start scrolling
            self._current_song = client_currentsong
            self._scrollingStrategy = ScrollingStrategy(self._lcd_display, self.LCD_LINES, self.LCD_ROWS, self.LCD_INTERNAL_BUFFER)
            self._scrollingStrategy.update_display(song_info.get_description())
        else: # Same song, check if scrolling is over, otherwise show songInfo and playerInfo
            if(not(self._scrollingStrategy.is_scrolling_ended())):
                self._scrollingStrategy.update_display(song_info.get_description())
            else:
                line1 = self.get_a_pretty_line(song_info.get_short_description())
                player_status_icon = self._player_info_state_to_icon_addr_dict[player_info.get_status()]
                #line2 = player_status_icon + " " +player_info.get_elapsed_time() \
                line2 = player_info.get_elapsed_time() + "   " + player_status_icon\
                        + "  " + chr(self.VOL_1_ADDRESS)+chr(self.VOL_2_ADDRESS) + player_info.get_volume()
                self._lcd_display.clear()
                self._lcd_display.message(line1 + "\n" + line2)

    def reset_screen(self):
        self._scrollingStrategy.force_end_scrolling()
        return self

    def execute_command_DOWN(self):
        self._mpd_client.connect(self._mpd_ip_address, 6600)
        client_status = self._mpd_client.status()
        player_info = PlayerInfo(client_status)
        self._mpd_client.setvol(max(int(player_info.get_volume())-1,0))
        self._mpd_client.disconnect()
        return self

    def execute_command_UP(self):
        self._mpd_client.connect(self._mpd_ip_address, 6600)
        client_status = self._mpd_client.status()
        player_info = PlayerInfo(client_status)
        self._mpd_client.setvol(min(int(player_info.get_volume())+1,100))
        self._mpd_client.disconnect()
        return self

    def execute_command_LEFT(self):
        self._mpd_client.connect(self._mpd_ip_address, 6600)
        client_status = self._mpd_client.status()
        self._mpd_client.previous()
        self._mpd_client.disconnect()
        return self

    def execute_command_RIGHT(self):
        self._mpd_client.connect(self._mpd_ip_address, 6600)
        client_status = self._mpd_client.status()
        self._mpd_client.next()
        self._mpd_client.disconnect()
        return self

    def execute_command_SELECT(self):
        self._mpd_client.connect(self._mpd_ip_address, 6600)
        client_status = self._mpd_client.status()
        player_info = PlayerInfo(client_status)
        if(player_info.is_stopped()):
            self._mpd_client.play(player_info.get_song_position_in_playlist())
        else:
            self._mpd_client.pause()
        self._mpd_client.disconnect()
        return self

    def execute_command_LEFT_AND_RIGHT(self):
        return TransientScreenDecorator.transform_in_transient(self.special_ops_screen, 30, self)



