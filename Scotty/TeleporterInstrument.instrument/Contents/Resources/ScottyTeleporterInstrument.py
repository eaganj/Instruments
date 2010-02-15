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