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

class Path(object):
    def __init__(self):
        self.color = None
        self.points = []
    
class ScottySMTest2GlassView(NSView):
    def __new__(cls, frame, instrument):
        return cls.alloc().initWithFrame_instrument_(frame, instrument)
        
    def initWithFrame_instrument_(self, frame, instrument):
        self = super(ScottySMTest2GlassView, self).initWithFrame_(frame)
        if not self:
            return self
        
        self._instrument = instrument
        self.reset()
        
        return self
        
    def addDrawPoint_(self, point):
        assert len(self._paths) > 0, "Must create a path before adding points to it."
        self._paths[-1].points.append(point)
        self.setNeedsDisplay_(True)
    
    def addPathWithColor_(self, color):
        path = Path()
        path.color = color
        self._paths.append(path)
        
    def reset(self):
        self._paths = []
        self.setNeedsDisplay_(True)
    
    @jre.debug.trap_exceptions
    def drawRect_(self, rect):
        self.drawPoints()
    
    def drawPoints(self):
        # Stop here if there's nothing to draw
        if not self._paths:
            return
        
        for stroke in self._paths:
            if not stroke.points:
                continue # Skip empty paths
            stroke.color.set()
            path = NSBezierPath.bezierPath()
            path.moveToPoint_(stroke.points[0])
            for point in stroke.points[1:]:
                path.lineToPoint_(point)
            
            path.stroke()
    
SMTest2GlassView = ScottySMTest2GlassView