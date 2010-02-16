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
            stroke.color.set()
            path = NSBezierPath.bezierPath()
            path.moveToPoint_(stroke.points[0])
            for point in stroke.points[1:]:
                path.lineToPoint_(point)
            
            path.stroke()
    
SMTest2GlassView = ScottySMTest2GlassView