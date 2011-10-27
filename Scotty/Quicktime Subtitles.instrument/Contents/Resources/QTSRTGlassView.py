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