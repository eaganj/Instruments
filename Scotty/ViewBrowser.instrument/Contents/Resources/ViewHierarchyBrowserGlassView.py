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