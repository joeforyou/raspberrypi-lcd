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
from AbstractMenuItemScreen import AbstractMenuItemScreen
from mpd import MPDClient


__author__ = 'diego'

class MoreSongInfosScreen(AbstractMenuItemScreen): # TODO Docs!

    def __init__(self, a_content, a_display):
        super(MoreSongInfosScreen, self).__init__("More Song\nInformations", a_display)
        self.set_backlight_colour_to_teal()
        self._mpd_client = MPDClient()
        self._mpd_client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self._mpd_client.idletimeout = None
        self._mpd_ip_address = "localhost"
        #self._mpd_ip_address = "192.168.178.42"
        # Interesting song info names
        self._interesting_song_keys = ['album',
                                       'artist',
                                       'title',
                                       'track',
                                       'pos',
                                       'time'
                                       'name',
                                       'file',
                                       ]
        # Interesting player stasus info names
        self._interesting_status_keys = ['playlistlength',
                                         'bitrate',
                                         'audio'
                                        ]
        self._infos_dict = {} # Dictonary to be shown on the display
        self._song_infos_dict = None # Song info dictionary from MPD
        self._player_status_dict = None # Player status dictionary from MPD
        self._current_info_index = 0

    def reset_screen(self):
        self._infos_dict = {}
        self._song_infos_dict = {}
        return self


    def update_content(self):
        self._mpd_client.connect(self._mpd_ip_address, 6600)
        song_infos_dict = self._mpd_client.currentsong()
        self._player_status_dict = self._mpd_client.status()
        self._mpd_client.disconnect()
        if(self._song_infos_dict <> song_infos_dict):
            self._current_info_index = 0
            self._song_infos_dict = song_infos_dict
            self._infos_dict = {}
            for a_key in self._interesting_song_keys:
                if(a_key in self._song_infos_dict):
                    self._infos_dict[a_key] = self._song_infos_dict[a_key]
            for a_key in self._interesting_status_keys:
                if(a_key in self._player_status_dict):
                    self._infos_dict[a_key] = self._player_status_dict[a_key]
        self._defaultContent = self.get_a_pretty_line(self._infos_dict.keys()[self._current_info_index]) + "\n" + \
                               self.get_a_pretty_line(self._infos_dict.get(self._infos_dict.keys()[self._current_info_index]))
        super(MoreSongInfosScreen, self).update_content()

    def execute_command_DOWN(self):
        if(self._current_info_index == len(self._infos_dict.keys()) - 1):
            self._current_info_index = 0
        else:
            self._current_info_index += 1
        return self

    def execute_command_UP(self):
        if(self._current_info_index == 0):
            self._current_info_index = len(self._infos_dict.keys()) - 1
        else:
            self._current_info_index -= 1
        return self

