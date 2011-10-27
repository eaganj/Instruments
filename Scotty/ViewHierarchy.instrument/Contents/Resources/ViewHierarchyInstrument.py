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