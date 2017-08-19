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
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

__author__ = 'diego'

class ScrollingStrategy(object):
    """
    This class is a strategy fro scrolling text over the Adafruit LCD screen.
    It is aware of the underlying Adafruit library, of the display size and it's buffer length.
     So it splits every string into an array of 40 character buffers, asking the display itself to scroll.
     The scrolling text appears only on the first line of the display due to limitation of the underlying API
    """

    def __init__(self, aDisplay, lines, columns, buffer):
        """
        Constructor to initialize the strategy

        :type aDisplay: Adafruit_CharLCDPlate
        :type lines: int
        :type columns: int
        :type buffer: int
        :param aDisplay: an instance of Adafruit_CharLCDPlate
        :param lines: number of lines of Adafruit_CharLCDPlate
        :param columns: number of columns of Adafruit_CharLCDPlate
        :param buffer: buffer size of Adafruit_CharLCDPlate
        """
        self._lcdDisplay = aDisplay
        self._display_lines = lines
        self._display_cols = columns
        self._buffer_length = buffer
        self._extra_display_length = self._buffer_length - self._display_cols # how many characters of the buffer are not displayed
        self._buffers = [] # array of buffers to be sent to the display
        self._buffers_index = 0 # index to be used to access the array of buffers
        self._fullContent = "" # the full content that should be scrolled over the display
        self._times_to_scroll_buffer = 0 # how many times a single buffer should scroll
        self._scrolling_ended = False


    def fill_buffers(self, content, buffers):
        """
        Recursively splits content into 40 character buffers, starting each buffer where
         the former stops scrolling

        :type content: str
        :type buffers: str[]
        :param content: content that should be scrolled over the display
        :param buffers: array of buffers to be sent to the display
        :return: buffers filled with the split content
        """
        if(len(content) > self._buffer_length):
            buffers.append(content[0:self._buffer_length])
            content = content[self._extra_display_length:]
            self.fill_buffers(content,buffers)
        else:
            buffers.append(content)
        return buffers

    def update_display(self,content):
        """
        Sends content to the display, asking the underlying API to scroll and substituting
        buffers when necessary

        :type content: str
        :param content:
        """
        if(self._fullContent != content): # Content is changed, must split in buffers
            self._scrolling_ended = False
            self._fullContent = content
            self.fill_buffers(content,self._buffers)
            self._buffers_index = 0
            self._times_to_scroll_buffer = self._extra_display_length
            self._lcdDisplay.clear()
            self._lcdDisplay.message(self._buffers[self._buffers_index])
        else: # Content hasn't changed, start scrolling
            if(self._times_to_scroll_buffer > 0):
                self._lcdDisplay.scrollDisplayLeft()
                self._times_to_scroll_buffer -= 1
            else: # A buffer has scrolled, move to next
                if(self._buffers_index < len(self._buffers)-1):
                    self._buffers_index += 1
                    self._times_to_scroll_buffer = self._extra_display_length
                    self._lcdDisplay.clear()
                    self._lcdDisplay.message(self._buffers[self._buffers_index])
                else: # Every buffer scrolled, do nothing
                    self._scrolling_ended = True

    def is_scrolling_ended(self):
        return  self._scrolling_ended

    def force_end_scrolling(self):
        self._scrolling_ended = True
        return self

    def estimate_cycles_to_scroll(self,content):
        estimate_buffers = []
        self.fill_buffers(content,estimate_buffers)
        return self._extra_display_length * len(estimate_buffers)


