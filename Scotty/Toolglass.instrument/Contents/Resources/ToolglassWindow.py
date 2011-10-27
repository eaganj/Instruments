# -*- coding: utf-8 -*-
#
# Scotty -- a meta-toolkit for runtime toolkit overloading
#
# Copyright 2009-2011, Université Paris-Sud
# by James R. Eagan (code at my last name dot me)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# and GNU Lesser General Public License along with this program.  
# If not, see <http://www.gnu.org/licenses/>.

from AppKit import *
from Foundation import *
import objc

from ScottyEventFunnel import *

# @EventFunnel
class ScottyToolglassWindow(EventFunnel(NSWindow)):
    def initWithContentRect_styleMask_backing_defer_(self, rect, mask, backing, defer):
        # NSBorderlessWindowMask
        # NSTitledWindowMask
        # NSClosableWindowMask
        # NSMiniaturizableWindowMask
        # NSResizableWindowMask
        # NSTexturedBackgroundWindowMask
        mask = NSTitledWindowMask|NSResizableWindowMask|NSClosableWindowMask|NSMiniaturizableWindowMask
        self = super(ScottyToolglassWindow, self).initWithContentRect_styleMask_backing_defer_(rect,
                                                                                               mask,
                                                                                               backing,
                                                                                               defer)
        if not self:
            return self
            
        self.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(0.49, 0.49, 0.55, 0.5))
        self.setOpaque_(False)
        
        return self

ToolglassWindow = ScottyToolglassWindow
__all__ = 'ToolglassWindow ScottyToolglassWindow'.split()