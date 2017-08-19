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
from subprocess import *
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

__author__ = 'diego'

class AbstractScreen(object):
    """
    This should be the top hierarchy class that represent a generic screen.
    Should be like a Java abstract class but I don't know how to write an abstract class in Python.
     Contains the attributes and methods commons to all the screens and a default implementation.
    """

    # LCD attributes
    LCD_ROWS = 16
    LCD_LINES = 2
    LCD_INTERNAL_BUFFER = 40

    # LCD Display buttons expressed in HEX so it's easier to compare with a bitmask
    NONE_LCD_BUTTON           = 0x00
    SELECT_LCD_BUTTON         = 0x01
    RIGHT_LCD_BUTTON          = 0x02
    DOWN_LCD_BUTTON           = 0x04
    UP_LCD_BUTTON             = 0x08
    LEFT_LCD_BUTTON           = 0x10
    UP_AND_DOWN_LCD_BUTTON    = 0x0C
    LEFT_AND_RIGHT_LCD_BUTTON = 0x12

    lcd_default_back_light = Adafruit_CharLCDPlate.TEAL # default LCD backlight colour

    def __init__(self, content, aDisplay):
        """
        Constructor to initialize a generic screen

        :type content: str
        :type aDisplay: Adafruit_CharLCDPlate
        :param content: the default content displayed by a generic screen
        :param aDisplay: an instance of Adafruit_CharLCDPlate
        """
        self._nextScreen = self
        self._previousScreen = self
        self._defaultContent = content
        self._lcd_display = aDisplay
        self._lcd_current_colour = self.lcd_default_back_light
        self._lcd_display.backlight(self.lcd_default_back_light)

    @property
    def lcd_display_instance(self):
        """
        This allows to access the real lcd display used by a screen.
        Useful for screen decorators


        :return: Adafruit_CharLCDPlate
        """
        return self._lcd_display

    @property
    def lcd_current_colour(self):
        return self._lcd_current_colour

    def set_backlight_colour_to_red(self):
        self._lcd_current_colour = self._lcd_display.RED
        self._lcd_display.backlight(self._lcd_display.RED)

    def set_backlight_colour_to_green(self):
        self._lcd_current_colour = self._lcd_display.GREEN
        self._lcd_display.backlight(self._lcd_display.GREEN)

    def set_backlight_colour_to_blue(self):
        self._lcd_current_colour = self._lcd_display.BLUE
        self._lcd_display.backlight(self._lcd_display.BLUE)

    def set_backlight_colour_to_yellow(self):
        self._lcd_current_colour = self._lcd_display.YELLOW
        self._lcd_display.backlight(self._lcd_display.YELLOW)

    def set_backlight_colour_to_teal(self):
        self._lcd_current_colour = self._lcd_display.TEAL
        self._lcd_display.backlight(self._lcd_display.TEAL)

    def set_backlight_colour_to_violet(self):
        self._lcd_current_colour = self._lcd_display.VIOLET
        self._lcd_display.backlight(self._lcd_display.VIOLET)

    def set_backlight_colour_to_white(self):
        self._lcd_current_colour = self._lcd_display.WHITE
        self._lcd_display.backlight(self._lcd_display.WHITE)


    def update_content(self):
        """
        Implementor should override this method to return the content displayed
        by a screen after a polling cycle. If no implementation is provided, default
         content is returned

        :return: default content if not overridden
        """
        self._lcd_display.clear()
        return self._lcd_display.message(self._defaultContent)

    def execute_command_UP(self):

        """
        When key UP_LCD_BUTTON on the display is pressed, this method is called.
        Implementors should hook up here operation to be performed and
        return the screen the should display the content returned by those operation.
        If no implementation is provided, the same screen instance is returned


        :return: self if no implementation is provided
        """
        return self

    def execute_command_DOWN(self):

        """
        When key DOWN_LCD_BUTTON on the display is pressed, this method is called.
        Implementors should hook up here operation to be performed and
        return the screen the should display the content returned by those operation.
        If no implementation is provided, the same screen instance is returned


        :return: self if no implementation is provided
        """
        return self

    def execute_command_LEFT(self):

        """
        When key LEFT_LCD_BUTTON on the display is pressed, this method is called.
        Implementors should hook up here operation to be performed and
        return the screen the should display the content returned by those operation.
        If no implementation is provided, the same screen instance is returned


        :return: self if no implementation is provided
        """
        return self

    def execute_command_RIGHT(self):

        """
        When key RIGHT_LCD_BUTTON on the display is pressed, this method is called.
        Implementors should hook up here operation to be performed and
        return the screen the should display the content returned by those operation.
        If no implementation is provided, the same screen instance is returned


        :return: self if no implementation is provided
        """
        return self

    def execute_command_SELECT(self):

        """
        When key SELECT_LCD_BUTTON on the display is pressed, this method is called.
        Implementors should hook up here operation to be performed and
        return the screen the should display the content returned by those operation.
        If no implementation is provided, the same screen instance is returned


        :return: self if no implementation is provided
        """
        return self

    def execute_command_UP_AND_DOWN(self):

        """
        When key UP_LCD_BUTTON and DOWN_LCD_BUTTON on the display are both pressed, this method is called.
        Implementors should hook up here operation to be performed and
        return the screen the should display the content returned by those operation.
        If no implementation is provided, the same screen instance is returned


        :return: self if no implementation is provided
        """
        return self

    def execute_command_LEFT_AND_RIGHT(self):

        """
        When key LEFT_LCD_BUTTON and RIGHT_LCD_BUTTON on the display are both pressed, this method is called.
        Implementors should hook up here operation to be performed and
        return the screen the should display the content returned by those operation.
        If no implementation is provided, the same screen instance is returned


        :return: self if no implementation is provided
        """
        return self

    def execute_command_NONE(self):

        """
        When no key at all  on the display is pressed, this method is called.
        Implementors should hook up here any operation needed when no one touches anything, eg.
        measuring seconds and eventually after a while passing automatically to another screen.
        If no implementation is provided, the same screen instance is returned


        :return: self if no implementation is provided
        """
        return self

    def poll_buttons(self):
        """
        This method execute the command corresponding to the key pressed on the display.
        Should be called every polling cycle and should not be overridden.
        Should be final if were Java, but I don't know how to mark final a method in Python


        :return: self
        """
        buttons_bitmap = self._lcd_display.buttons()
        if(buttons_bitmap == self.NONE_LCD_BUTTON):
            return self.execute_command_NONE()
        if(buttons_bitmap == self.UP_LCD_BUTTON):
            return self.execute_command_UP()
        if(buttons_bitmap == self.DOWN_LCD_BUTTON):
            return self.execute_command_DOWN()
        if(buttons_bitmap == self.LEFT_LCD_BUTTON):
            return self.execute_command_LEFT()
        if(buttons_bitmap == self.RIGHT_LCD_BUTTON):
            return self.execute_command_RIGHT()
        if(buttons_bitmap == self.SELECT_LCD_BUTTON):
            return self.execute_command_SELECT()
        if(buttons_bitmap == self.LEFT_AND_RIGHT_LCD_BUTTON):
            return self.execute_command_LEFT_AND_RIGHT()
        if(buttons_bitmap == self.UP_AND_DOWN_LCD_BUTTON):
            return self.execute_command_UP_AND_DOWN()
        return self

    def poll_keys_and_update_display(self):
        """
        This is and only this should be the method invoked during the polling cycle.
        It's the method that correctly polls for any button pressed, executes the requested action
         and asks to the current screen to update the message shown on the LCD display
        Should be called every polling cycle and should not be overridden.
        Should be final if were Java, but I don't know how to mark final a method in Python


        :return: the next screen the will be polled, as returned by the poll_buttons() method
        """
        next_target_screen = self.poll_buttons()
        next_target_screen.update_content()
        if(next_target_screen <> self):
            self.reset_screen()
        return next_target_screen

    def reset_screen(self):
        """
        If a screen has some kind of internal state that should be set before passing control to another screen,
        this method should be implemented

        :return: AbstractScreen
        """
        return self

    def get_a_pretty_line(self, aString):
        """
        Convenience method to transform a generic string to one that appears pretty on the LCD display.
        If the string is shorter than the display, it is centered.
        Otherwise the last two characters are substituted with two dots.


        :type aString: str
        :param aString:
        :return: str
        """
        string_length = len(aString)
        if(string_length < self.LCD_ROWS):
            empty_space = self.LCD_ROWS - string_length
            return " "*(empty_space/2) + aString
        elif(string_length > self.LCD_ROWS):
            return aString[:self.LCD_ROWS-2] + "."*2
        return aString


    def run_shell_command(self, aCommand):

        """
        Method that runs a command on the shell

        :param aCommand: a command to be executed by the operative system's shell
        :return: the output of the command
        """
        p = Popen(aCommand, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output
