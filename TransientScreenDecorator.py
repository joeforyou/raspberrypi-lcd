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

class TransientScreenDecorator(AbstractScreen):

    def __init__(self,transient_screen, expires_in, permanent_screen):
        """
        This is a decorator that makes a screen temporary, so that after a number of polling cycles
        "decades" in a different permanent screen.
        It's useful when you want a transition to another screen when nobody presses any botton for  while

        :type transient_screen: AbstractScreen
        :type expires_in: int
        :type permanent_screen: AbstractScreen
        :param transient_screen: the screen that must be transient
        :param expires_in: number of polling cycles before the transition to the permanent screen
        :param permanent_screen: the permanent screen that appears after the transition
        """
        super(TransientScreenDecorator, self).__init__(transient_screen._defaultContent, transient_screen.lcd_display_instance)
        self._expiring_screen = transient_screen
        self._default_screen = permanent_screen
        self._poll_cycles_before_expires = self._cycles_counter = expires_in
        self._lcd_display.backlight(transient_screen.lcd_current_colour)

    def update_content(self):
        self._expiring_screen.update_content()

    def execute_command_NONE(self):
        # Nothing happened, must decide to which screen the command should be sent
        if(self._cycles_counter > 0):
            self._cycles_counter -= 1
            target_screen = self._expiring_screen.execute_command_NONE()
            if (target_screen == self._expiring_screen):
                return self
            else:
                self._expiring_screen.reset_screen()
                return target_screen # if screen has changed, return the new one
        # Screen is expired, reset the transient and return the permanent
        self._expiring_screen.reset_screen()
        return self._default_screen.execute_command_NONE()

    def execute_command_UP(self):
        # A button is pressed, reset the counter and ask the temporary screen to execute the command
        self._cycles_counter = self._poll_cycles_before_expires
        target_screen = self._expiring_screen.execute_command_UP()
        return self if (target_screen == self._expiring_screen) else target_screen # if screen has changed, return the new one

    def execute_command_DOWN(self):
        # A button is pressed, reset the counter and ask the temporary screen to execute the command
        self._cycles_counter = self._poll_cycles_before_expires
        target_screen = self._expiring_screen.execute_command_DOWN()
        return self if (target_screen == self._expiring_screen) else target_screen # if screen has changed, return the new one

    def execute_command_LEFT(self):
        # A button is pressed, reset the counter and ask the temporary screen to execute the command
        self._cycles_counter = self._poll_cycles_before_expires
        target_screen = self._expiring_screen.execute_command_LEFT()
        return self if (target_screen == self._expiring_screen) else target_screen # if screen has changed, return the new one

    def execute_command_RIGHT(self):
        # A button is pressed, reset the counter and ask the temporary screen to execute the command
        self._cycles_counter = self._poll_cycles_before_expires
        target_screen = self._expiring_screen.execute_command_RIGHT()
        return self if (target_screen == self._expiring_screen) else target_screen # if screen has changed, return the new one

    def execute_command_LEFT_AND_RIGHT(self):
        # A button is pressed, reset the counter and ask the temporary screen to execute the command
        self._cycles_counter = self._poll_cycles_before_expires
        target_screen = self._expiring_screen.execute_command_LEFT_AND_RIGHT()
        return self if (target_screen == self._expiring_screen) else target_screen # if screen has changed, return the new one

    def execute_command_UP_AND_DOWN(self):
        # A button is pressed, reset the counter and ask the temporary screen to execute the command
        self._cycles_counter = self._poll_cycles_before_expires
        target_screen = self._expiring_screen.execute_command_UP_AND_DOWN()
        return self if (target_screen == self._expiring_screen) else target_screen # if screen has changed, return the new one

    def execute_command_SELECT(self):
        # A button is pressed, reset the counter and ask the temporary screen to execute the command
        self._cycles_counter = self._poll_cycles_before_expires
        target_screen = self._expiring_screen.execute_command_SELECT()
        return self if (target_screen == self._expiring_screen) else target_screen # if screen has changed, return the new one

    @classmethod
    def transform_in_transient(cls, screen_to_become_transient, poll_cycles_before_expire, permanent_screen):
        """
        A factory method useful to transform a screen in a transient one without knowing how to
         create a TransientScreenDecorator

        :type screen_to_become_transient: AbstractScreen
        :type poll_cycles_before_expire: int
        :type permanent_screen: AbstractScreen
        :param screen_to_become_transient: the screen that must become a transient screen
        :param poll_cycles_before_expire: number of polling cycles before the transition to the permanent screen
        :param permanent_screen: the permanent screen that appears after the transition
        :return:
        """
        return TransientScreenDecorator(screen_to_become_transient, poll_cycles_before_expire, permanent_screen)