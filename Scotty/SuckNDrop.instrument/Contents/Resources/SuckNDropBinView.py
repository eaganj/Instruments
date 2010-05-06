from AppKit import *
from Foundation import *
import objc



### NOT CURRENTLY USED!


class ScottySuckNDropBinView(NSView):
    def __new__(cls, frame, instrument):
        # Pythonic constructor
        return cls.alloc().initWithFrame_instrument_(frame, instrument)
        
    def initWithFrame_instrument_(self, frame, instrument):
        self = super(ScottySuckNDropBinView, self).initWithFrame_(frame)
        if not self:
            return self
            
        self.instrument = instrument
        
        return self
        
    def drawRect_(self, rect):
        fillColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.25, 0.25, 0.30, 0.70)
        strokeColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0.30, 0.30, 0.35, 0.80)
        
        fillColor.set()
        NSRectFill(rect)
        strokeColor.set()
        NSFrameRect(rect)
        
        

SuckNDropBinView = ScottySuckNDropBinView

__all__ = 'SuckNDropBinView ScottySuckNDropBinView'.split()