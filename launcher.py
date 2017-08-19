#!/usr/bin/python
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
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from NowPlayingScreen import NowPlayingScreen
from ShutdownScreen import ShutdownScreen
from ShowIpScreen import ShowIpScreen
from ShowDateAndTimeScreen import ShowDateAndTimeScreen
from MenuScreen import MenuScreen
from MoreSongInfosScreen import MoreSongInfosScreen
from WelcomeScreen import WelcomeScreen

__author__ = 'diego'
aDisplay = Adafruit_CharLCDPlate()
# Welcome message
currentScreen = WelcomeScreen("", aDisplay)
for i in range(1,16):
    currentScreen = currentScreen.poll_keys_and_update_display()
    sleep(0.25)
aDisplay.clear()
menuScreen = MenuScreen("", aDisplay)
menuScreen.add_menu_item(MoreSongInfosScreen("", aDisplay))
menuScreen.add_menu_item(ShowDateAndTimeScreen("", aDisplay))
menuScreen.add_menu_item(ShowIpScreen("", aDisplay).set_interface_to_eth())
menuScreen.add_menu_item(ShowIpScreen("", aDisplay).set_interface_to_wlan())
menuScreen.add_menu_item(ShutdownScreen("", aDisplay))
playingScreen = NowPlayingScreen("", aDisplay)
playingScreen.special_ops_screen = menuScreen
menuScreen.permanent_screen = playingScreen
currentScreen = playingScreen

print(currentScreen)
while True:
    currentScreen = currentScreen.poll_keys_and_update_display()
    sleep(0.25)