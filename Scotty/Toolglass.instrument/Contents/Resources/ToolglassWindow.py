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