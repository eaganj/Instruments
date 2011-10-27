# -*- coding: utf-8 -*-
#
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
    
    def activate(self, context):
        super(ScottyViewHierarchyBrowserInstrument, self).activate(context)
        if not self._controller:
            self._controller = ViewHierarchyBrowserController.alloc().initWithInstrument_(self)
        self._controller.showWindow_(self)
        
        glassWindows = context.attachGlassWindowToAllWindows(interactive=False)
        for glassWindow in glassWindows:
            parentWindow = glassWindow.parentWindow()
            glassWindow.setContentView_(ViewHierarchyBrowserGlassView(parentWindow.frame(), self))
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
        # glassView = instrumentManager.glassViewForWindow(widget.window())
        glassView = self.context.glassViewForWindow(widget.window())
        if glassView:
            glassView.highlightWidget_(widget)
    
    def highlightWindow(self, window):
        widget = window.contentView().superview()
        self.highlightWidget(widget)
        
    
ViewHierarchyBrowserInstrument = ScottyViewHierarchyBrowserInstrument

__all__ = 'ViewHierarchyBrowserInstrument ScottyViewHierarchyBrowserInstrument'.split()