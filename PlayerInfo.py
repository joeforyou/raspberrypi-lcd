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

class PlayerInfo(object):
    '''
    Class that represent the MPD current status
    '''
    STOP = 0
    PLAY = 1
    PAUSE = 2

    def __init__(self, mpd_info_dictionary):
        '''
        This constructor accepts a dictionary of infos that comes from MPDClient.

        :type mpd_info_dictionary: dict
        :param mpd_info_dictionary:

        '''
        self._states_dict = {'stop':self.STOP, 'play':self.PLAY, 'pause':self.PAUSE}
        self._elapsed_in_sec = 0
        self._state = self._states_dict[mpd_info_dictionary.get('state','stop')]
        self._song_position_in_playlist = int(mpd_info_dictionary.get('song',0))
        self._playlist_lenght = mpd_info_dictionary.get('playlistlength',0)
        self._volume = mpd_info_dictionary.get('volume',0)
        if('elapsed' in mpd_info_dictionary):
            self._elapsed_in_sec = int(mpd_info_dictionary['elapsed'].split(".")[0])

    def get_elapsed_time(self):
        if(self._elapsed_in_sec < 3600):
            m, s = divmod(self._elapsed_in_sec, 60)
            return "%02d:%02d" % (m, s)
        else:
            m, s = divmod(self._elapsed_in_sec, 60)
            h, m = divmod(m, 60)
            return "%02d:%02d" % (h, m)

    def get_volume(self):
        return self._volume

    def get_status(self):
        return self._state

    def get_playlist_length(self):
        return int(self._playlist_lenght)

    def get_playlist_progression(self):
        return "%d/" % (self._song_position_in_playlist+1) + self._playlist_lenght

    def get_song_position_in_playlist(self):
        return self._song_position_in_playlist

    def is_playing(self):
        return self._state == self.PLAY

    def is_stopped(self):
        return self._state == self.STOP

    def is_paused(self):
        return self._state == self.PAUSE