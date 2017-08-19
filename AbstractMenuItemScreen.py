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

class AbstractMenuItemScreen(AbstractScreen):
    '''
    This should be the top hierarchy class that represent a generic screen that can be inserted in a menu list rendered by
    a MenuScreen.
    Should be like a Java abstract class but I don't know how to write an abstract class in Python.
     Contains the attributes and methods commons to all the screens that can be part of a menu and a default implementation.

    '''

    def __init__(self, a_description, a_menu_screen, a_content, a_display):
        """
        Constructor to initialize instance

        :type a_description: str
        :type a_menu_screen: AbstractScreen
        :type a_content: str
        :type a_display: Adafruit_CharLCDPlate
        :param a_description: the description returned when displayed as a menu item
        :param a_menu_screen: the surrounding menu screen
        :param a_content: generic content
        :param a_display: an instance of Adafruit_CharLCDPlate
        """
        super(AbstractMenuItemScreen, self).__init__(a_content, a_display)
        self._menu_item_description = a_description
        self._enclosing_menu = a_menu_screen

    def __init__(self, a_content, a_display):
        """
        :type a_content: str
        :type a_display: Adafruit_CharLCDPlate

        :param a_content: the description returned when displayed as a menu item
        :param a_display: an instance of Adafruit_CharLCDPlate
        """
        super(AbstractMenuItemScreen, self).__init__(a_content, a_display)
        self._menu_item_description = a_content if a_content.strip() <> "" else "No desc avail."
        self._enclosing_menu = None

    @property
    def menu_description(self):
        return self._menu_item_description

    @menu_description.setter
    def menu_description(self, a_description):
        self._menu_item_description = a_description

    @property
    def enclosing_menu(self):
        return self._enclosing_menu

    @enclosing_menu.setter
    def enclosing_menu(self,a_screen):
        """
        :rtype : AbstractScreen
        :param a_screen:
        """
        self._enclosing_menu = a_screen

    def execute_command_LEFT(self):
        return self._enclosing_menu
