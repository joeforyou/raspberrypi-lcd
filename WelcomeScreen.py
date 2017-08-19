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
from AbstractScreen import AbstractScreen

__author__ = 'diego'

class WelcomeScreen(AbstractScreen):
    '''
    This class serves as a welcome screen to the app.
    '''
    # Custom characters

    # Animation frameS
    FRAME_1 = [0b00000,
               0b00000,
               0b01110,
               0b11001,
               0b10101,
               0b10001,
               0b01110]

    FRAME_2 = [0b00000,
               0b00000,
               0b01110,
               0b10011,
               0b10101,
               0b10001,
               0b01110]

    FRAME_3 = [0b00000,
               0b00000,
               0b01110,
               0b10001,
               0b10101,
               0b10011,
               0b01110]

    FRAME_4 = [0b00000,
               0b00000,
               0b01110,
               0b10001,
               0b10101,
               0b11001,
               0b01110]

    # Custom characters address on LCD RAM
    FRAME_1_ADDRESS = 0x01
    FRAME_2_ADDRESS = 0x02
    FRAME_3_ADDRESS = 0x03
    FRAME_4_ADDRESS = 0x04

    def __init__(self, a_content, a_display):
        super(WelcomeScreen, self).__init__(a_content, a_display)
        self._animation = [self.FRAME_1_ADDRESS, self.FRAME_2_ADDRESS, self.FRAME_3_ADDRESS, self.FRAME_4_ADDRESS]
        self._lcd_display.createChar(self.FRAME_1_ADDRESS, self.FRAME_1)
        self._lcd_display.createChar(self.FRAME_2_ADDRESS, self.FRAME_2)
        self._lcd_display.createChar(self.FRAME_3_ADDRESS, self.FRAME_3)
        self._lcd_display.createChar(self.FRAME_4_ADDRESS, self.FRAME_4)
        self._i = 0
        self._j = 2
        self._defaultContent = self.get_a_pretty_line("Welcome to") + "\n" \
                               + self.get_a_pretty_line("V" + chr(self._animation[self._i]) + "lumi" + chr(self._animation[self._j]))

    def update_content(self):
        self._i = (self._i + 1) % 4
        self._j = (self._j + 1) % 4
        self._defaultContent = self.get_a_pretty_line("Welcome to") + "\n" \
                               + self.get_a_pretty_line("V" + chr(self._animation[self._i]) + "lumi" + chr(self._animation[self._j]))
        super(WelcomeScreen, self).update_content()
