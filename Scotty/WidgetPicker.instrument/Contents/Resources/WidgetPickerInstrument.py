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

from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

from collections import deque

import jre.cocoa
import jre.debug

#from DecoratorWindow import *
#from IIKit import GlassWindow
#from PickerInstrument import *
#from InstrumentManager import *
from IIKit.scotty import *
from WidgetProtocol import *

class ScottyWidgetPickerInstrument(PickerInstrument):
    name = u"Widget Picker"
    verb = u"Pick widget"
    
    @classmethod
    def objectAtPointInWindow(cls, point, window):
        ''' 
        Return the object, if any, at `point`. 
        
        If `window` is None, `point` is expressed in screen coordinates.  Otherwise, `point` is taken to
        be in that window's coordinates.
        '''
        slocation = point
        if window:
            slocation = window.convertBaseToScreen_(point)
            wlocation = point
        else:
            window = cls._windowAtLocation(slocation)
            wlocation = window.convertScreenToBase_(slocation)
            
        if window:
            return cls.widgetAtLocationInWindow(wlocation, window)
        else:
            return None
            
    @classmethod
    def _windowAtLocation(cls, location):
        for window in NSApp().orderedWindows():
            if isinstance(window, (GlassWindow,)) or not window.isVisible():
                # Only include real, visible windows
                continue

            if NSMouseInRect(location, window.frame(), False):
                return window

        return None
    
    @classmethod
    def widgetAtLocationInWindow(cls, location, window):
        view = window.contentView().superview()
        frame = view.convertRectToBase_(view.convertRect_fromView_(view.frame(), view.superview()))
        if not NSMouseInRect(location, frame, False):
            result = None
        else:
            hit = view.hitTest_(location)
            if WidgetProtocol.objectConforms_(hit):
                result = hit
            else:
                result = None
        return result

WidgetPickerInstrument = ScottyWidgetPickerInstrument

__all__ = 'ScottyWidgetPickerInstrument WidgetPickerInstrument'.split()