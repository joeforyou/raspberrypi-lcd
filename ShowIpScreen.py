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

__author__ = 'diego'

class ShowIpScreen(AbstractMenuItemScreen):

    ETH0 = 0
    WLAN0 = 1
    _eth0_command = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    _wlan0_command = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    _commands = {ETH0:_eth0_command, WLAN0:_wlan0_command}
    _descriptions = {ETH0:"Show eth\nIP address", WLAN0:"Show wifi\nIP address"}

    def __init__(self, a_description, a_menu_screen):
        super(ShowIpScreen, self).__init__("Show eth\nIP address", a_menu_screen)
        self.set_backlight_colour_to_green()
        self._interface = self.ETH0
        ip_addr = self.run_shell_command(self._commands.get(self._interface))
        self._defaultContent = self.get_a_pretty_line(ip_addr if ip_addr <> "" else "No IP Address")

    def update_content(self):
        ip_addr = self.run_shell_command(self._commands.get(self._interface))
        self._defaultContent = self.get_a_pretty_line(ip_addr if ip_addr <> "" else "No IP Address")
        super(ShowIpScreen, self).update_content()

    def set_interface_to_eth(self):
        self._interface = self.ETH0
        self.menu_description = self._descriptions.get(self._interface)
        return self

    def set_interface_to_wlan(self):
        self._interface = self.WLAN0
        self.menu_description = self._descriptions.get(self._interface)
        return self


