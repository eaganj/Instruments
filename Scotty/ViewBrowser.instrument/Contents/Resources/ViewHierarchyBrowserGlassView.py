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

from AppKit import *
from Foundation import *
import objc

import jre.cocoa
import jre.debug

class ScottyViewHierarchyBrowserGlassView(NSView):
    def __new__(cls, frame, instrument):
        return cls.alloc().initWithFrame_instrument_(frame, instrument)
        
    def initWithFrame_instrument_(self, frame, instrument):
        self = super(ScottyViewHierarchyBrowserGlassView, self).initWithFrame_(frame)
        if not self:
            return self
        
        self._instrument = instrument
        self.reset()
        
        return self
        
    def highlightWidget_(self, widget):
        # FIXME
        self.reset()
        self._boxes.append((widget, 0))
        self.setNeedsDisplay_(True)
        
    def reset(self):
        self._boxes = []
        self.setNeedsDisplay_(True)
    
    @jre.debug.trap_exceptions
    def drawRect_(self, rect):
        self.drawWidgetRects()
    
    def drawWidgetRects(self):
        # Stop here if there's nothing to draw
        if not self._boxes:
            return
        
        fillColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.0, 0.0, 1.0, 0.20)
        strokeColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.0, 0.0, 1.0, 0.15)
        for view, level in self._boxes:
            box = self.convertRect_fromView_(view.convertRectToWindow_(view.frame()), None)
            fillColor.set()
            NSBezierPath.fillRect_(box)
            strokeColor.set()
            NSBezierPath.strokeRect_(box)
    
ViewHierarchyBrowserGlassView = ScottyViewHierarchyBrowserGlassView