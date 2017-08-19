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
__author__ = 'diego'

class SongInfo(object):
    '''
    Class that represent the current song played
    '''

    def __init__(self, mpd_info_dictionary):
        """
        This constructor accepts a dictionary of infos that comes from MPDClient.

        :type mpd_info_dictionary: dict
        :param mpd_info_dictionary:
        """
        self._file = False
        self._radio = False
        self._airport = False
        if(("track") in mpd_info_dictionary): # we're playing a song from file
            self._album = mpd_info_dictionary.get('album','')
            self._artist = mpd_info_dictionary.get('artist','')
            self._time = mpd_info_dictionary.get('time')
            self._title = mpd_info_dictionary.get('title')
            self._track = mpd_info_dictionary.get('track','')
            self._description = str(self._artist) + " - " + self._album + " - " + self._title
            self._short_description = self._title
            self._file = True
        elif("title" in mpd_info_dictionary): # we're listening to an internet radio
            self._title = mpd_info_dictionary.get('title','')
            self._name = mpd_info_dictionary.get('name','')
            self._radio = True
            self._description = self._name + " - " + self._title
            self._short_description = self._title
        else: # a communication error, or maybe shairport in use
            self._album = ""
            self._title = ""
            self._track = ""
            self._artist = ""
            self._time = 0
            self._name = ""
            self._description = "No Playlist"
            self._short_description = "No Playlist"
            #TODO: Airport

    def is_file(self):
        return self._file

    def is_radio(self):
        return self._radio

    def is_airport(self):
        return self._airport

    def get_description(self):
        return self._description

    def get_short_description(self):
        return self._short_description

    def __str__(self):
        return self.get_description()

