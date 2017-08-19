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
from time import strftime
from datetime import datetime

__author__ = 'diego'

class ShowDateAndTimeScreen(AbstractMenuItemScreen):

    def __init__(self, a_content, a_display):
        super(ShowDateAndTimeScreen, self).__init__("Show Date\nand Time", a_display)
        self.set_backlight_colour_to_yellow()
        self._time_format = '%H:%M:%S'
        self._date_format = '%a %d %b %Y'
        #self._defaultContent = datetime.now().strftime('%d/%m/%Y  %H:%M:%S')
        self._defaultContent = self.get_a_pretty_line(datetime.now().strftime(self._date_format)) + "\n" \
                               + self.get_a_pretty_line(datetime.now().strftime(self._time_format))

    def update_content(self):
        self._defaultContent = self.get_a_pretty_line(datetime.now().strftime(self._date_format)) + "\n" \
                               + self.get_a_pretty_line(datetime.now().strftime(self._time_format))
        super(ShowDateAndTimeScreen,self).update_content()

