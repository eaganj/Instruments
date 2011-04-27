from __future__ import with_statement

from Foundation import *
from AppKit import *
import objc

import jre.cocoa
import jre.debug

#from Instrument import *
from IIKit import *
from ViewHierarchyGlassView import *

class ScottyViewHierarchyInstrument(Instrument):
    name = u"Widget Hierarchy Viewer" # FIXME refactor
    verb = u"Show widget hierarchy"
    
    def wantsGlassWindow(self):
        return True
        
    def newGlassViewForGlassWindow(self, glassWindow):
        window = glassWindow.parentWindow()
        print " glassWindow:", glassWindow
        print "parentwindow:", window
        view = ViewHierarchyGlassView(window.frame(), self)
        self._traverseWidgetTreeForWindow(window, view)
        return view
    
    def _traverseWidgetTreeForWindow(self, window, glassView):
        self._traverseWidgetTreeForWidget(window.contentView().superview(), glassView)
    
    def _traverseWidgetTreeForWidget(self, widget, glassView, level=0):
        glassView.addWidget_atLevel_(widget, level)
        for view in widget.subviews():
            self._traverseWidgetTreeForWidget(view, glassView, level+1)

    def shouldHijackInteraction(self):
        return True
                
    def mouseUp(self, event):
        if self._activatedOnce:
            self.deactivate()
        
    
ViewHierarchyInstrument = ScottyViewHierarchyInstrument

__all__ = 'ViewHierarchyInstrument ScottyViewHierarchyInstrument'.split()