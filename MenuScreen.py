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
from TransientScreenDecorator import TransientScreenDecorator
from AbstractScreen import AbstractScreen
from NowPlayingScreen import NowPlayingScreen

__author__ = 'diego'


class MenuScreen(AbstractScreen):
    '''
    This is a screen that can be used as a menu. Menu element must be concrete subclasses of AbstractMenuItemScreen.
    UP and DOWN keys must be used to scroll through the menu item list, SELECT or RIGHT keys to enter into an item,
    LEFT to come back to the menu list.
    It is possible to define a screen to display after the menu or a menu item remains untouched for 30 polling cycles
    '''

    def __init__(self, a_content, a_display):
        """
        :type a_content: str
        :type a_display: Adafruit_CharLCDPlate
        :param a_content: generic content
        :param a_display: an instance of Adafruit_CharLCDPlate
        """
        super(MenuScreen,self).__init__(a_content, a_display)
        self._poll_cycles_before_item_expires = 30
        self._menu_items = []
        self._current_item = 0
        self._permanent_screen_after_menu_item = self #It's possible to display a screen if nothing happens for 30 polling cycles, this is the default impl
        self._transient_self = self

    def init_screen_list(self):
        for item in self._menu_items:
            item.enclosing_menu = self._transient_self

    @property
    def permanent_screen(self):
        return self._permanent_screen_after_menu_item

    @permanent_screen.setter
    def permanent_screen(self, a_screen):
        self._permanent_screen_after_menu_item = a_screen
        self._transient_self = TransientScreenDecorator.transform_in_transient(self, 30, self._permanent_screen_after_menu_item)
        self.init_screen_list()

    @property
    def menu_item_list(self):
        return self._menu_items

    @menu_item_list.setter
    def menu_item_list(self, a_menu_item_screen_list):
        self._menu_items = a_menu_item_screen_list
        self.init_screen_list()

    def add_menu_item(self, a_menu_item_screen):
        a_menu_item_screen.enclosing_menu = self._transient_self
        self._menu_items.append(a_menu_item_screen)

    def reset_screen(self): # back to the first menu item
        self._current_item = 0
        return self

    def update_content(self):
        self.set_backlight_colour_to_violet()
        self._lcd_display.clear()
        self._lcd_display.message("%d. %s" % (self._current_item + 1, self._menu_items[self._current_item].menu_description))

    def execute_command_UP(self):
        if(self._current_item == 0):
            self._current_item = len(self._menu_items) - 1
        else:
            self._current_item -= 1
        return self

    def execute_command_DOWN(self):
        if(self._current_item == len(self._menu_items) - 1):
            self._current_item = 0
        else:
            self._current_item += 1
        return self

    def execute_command_RIGHT(self):
        return TransientScreenDecorator.transform_in_transient(self._menu_items[self._current_item], self._poll_cycles_before_item_expires, self._permanent_screen_after_menu_item)

    def execute_command_SELECT(self):
        return TransientScreenDecorator.transform_in_transient(self._menu_items[self._current_item], self._poll_cycles_before_item_expires, self._permanent_screen_after_menu_item)

