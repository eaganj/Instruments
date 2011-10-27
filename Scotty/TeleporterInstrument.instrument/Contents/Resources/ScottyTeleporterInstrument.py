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

import jre.cocoa
import jre.debug

from WidgetPickerInstrument import *
from ScottyController import *

class ScottyTeleporterInstrument(ScottyWidgetPickerInstrument):
    name = u"Widget Teleporter" # FIXME refactor
    verb = u"Choose teleportation view"
    
    def __init__(self):
        super(ScottyTeleporterInstrument, self).__init__()
        
        self.action = self.telportWidget
    
    def telportWidget(self, widget):
        print 'teleport widget', widget
        # FIXME: refactor WindowEmitter class
        emitter = Scotty().sharedSender()
        window = widget.window()
        emitter.enableHook_forWindow_(True, window)
        
        widgetFrameInWindowCoords = widget.convertRectToWindow_(widget.frame())
        # Convert to graphics origin
        ((cx, cy), (cw, ch)) = widgetFrameInWindowCoords
        ((wx, wy), (ww, wh)) = window.frame()
        widgetFrameInWindowCoords = NSMakeRect(cx, wh - (cy + ch), cw, ch)
        
        emitter.addClippingRegion_forWindow_(widgetFrameInWindowCoords, window)
        
            
TeleporterInstrument = ScottyTeleporterInstrument

#__all__ = 'ScottyWidgetPickerInstrument WidgetPickerInstrument'.split()