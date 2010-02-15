from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

import jre.cocoa
import jre.debug

from IIKit import *
from ViewHierarchyBrowserController import *
from ViewHierarchyBrowserGlassView import *

class ScottyViewHierarchyBrowserInstrument(Instrument):
    name = u"Widget Hierarchy Browser" # FIXME refactor
    verb = u"Browse widget hierarchy"
    
    def __init__(self):
        super(ScottyViewHierarchyBrowserInstrument, self).__init__()
        
        self._controller = None
    
    def wantsGlassWindow(self):
        return True
        
    def newGlassViewForGlassWindow(self, glassWindow):
        window = glassWindow.parentWindow()
        view = ViewHierarchyBrowserGlassView(window.frame(), self)
        return view

    def shouldHijackInteraction(self):
        return False
    
    def activate(self):
        super(ScottyViewHierarchyBrowserInstrument, self).activate()
        if not self._controller:
            self._controller = ViewHierarchyBrowserController.alloc().initWithInstrument_(self)
        self._controller.showWindow_(self)
        self.deactivate() # FIXME: this should happen on window close!
                
    def mouseUp(self, event):
        if self._activatedOnce:
            self.deactivate()
    
    def highlightWidget(self, widget):
        if isinstance(widget, NSWindow):
            self.highlightWindow(widget)
            return
            
        window = widget.window()
        instrumentManager = InstrumentManager.sharedInstrumentManager()
        instrumentManager.resetGlassViewsForInstrument_(self)
        glassView = instrumentManager.glassViewForWindow(widget.window())
        if glassView:
            glassView.highlightWidget_(widget)
    
    def highlightWindow(self, window):
        widget = window.contentView().superview()
        self.highlightWidget(widget)
        
    
ViewHierarchyBrowserInstrument = ScottyViewHierarchyBrowserInstrument

__all__ = 'ViewHierarchyBrowserInstrument ScottyViewHierarchyBrowserInstrument'.split()