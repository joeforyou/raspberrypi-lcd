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
from time import sleep


__author__ = 'diego'

class ShutdownScreen(AbstractMenuItemScreen):

    def __init__(self, aContent, aDisplay):
        super(ShutdownScreen,self).__init__("Shutdown\nSystem...", aDisplay)
        self.set_backlight_colour_to_red()
        self._defaultContent = self.get_a_pretty_line("Press \'select\'") +"\n"+ self.get_a_pretty_line("to shutdown")

    def execute_command_SELECT(self):
        self.set_backlight_colour_to_red()
        self.run_shell_command("mpc stop")
        self._defaultContent = "Wait 10 seconds\nthen switch off"
        self.update_content()
        sleep(4)
        self.run_shell_command("sudo shutdown -h now")
        sleep(1.5)
        self._lcd_display.noDisplay()
        self._lcd_display.backlight(self._lcd_display.OFF)
        return self