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
    
class QTSRTGlassView(NSView):
    def __new__(cls, frame, instrument):
        return cls.alloc().initWithFrame_instrument_(frame, instrument)
        
    def initWithFrame_instrument_(self, frame, instrument):
        self = super(QTSRTGlassView, self).initWithFrame_(frame)
        if not self:
            return self
        
        self._instrument = instrument
        self.reset()
        
        return self
        
    def reset(self):
        self._paths = []
        self.setNeedsDisplay_(True)
    
    
class QTSRTLayerDelegate(NSObject):
    def __new__(cls, layer): # Pythonic constructor
        return cls.alloc().initWithLayer_(layer)
        
    def initWithLayer_(self, layer):
        self = super(QTSRTLayerDelegate, self).init()
        if not self:
            return self
        
        self._layer = layer
        self.reset()
        
        return self
        
    def drawLayer_inContext_(self, layer, context):
        graphicsContext = NSGraphicsContext.graphicsContextWithGraphicsPort_flipped_(context, False)
        NSGraphicsContext.saveGraphicsState()
        NSGraphicsContext.setCurrentContext_(graphicsContext)
        try:
            # self.draw()
            pass
        finally:
            NSGraphicsContext.restoreGraphicsState()