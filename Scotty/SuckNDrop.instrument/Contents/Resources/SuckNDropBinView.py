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