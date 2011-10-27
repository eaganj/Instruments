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

from AppKit import *
from Foundation import *
import objc

from ToolglassWindow import *
from IIKit.InstrumentLoader import InstrumentLoader

# Keep a copy of the currentBundle when this module was loaded.  We do this so that subclasses
# loaded from another plugin bundle will still be able to find nibs defined in *our* bundle
_bundle_ = InstrumentLoader.currentBundle 

class ScottyToolglassWindowController(NSWindowController):
    def __new__(cls, instrument):
        return cls.alloc().initWithInstrument_(instrument)
        
    def initWithInstrument_(self, instrument):
        self = self._initWindowNibWithOwner_(self)
        if not self:
            return self
        
        self.__instrument = instrument
        
        return self
    
    def _initWindowNibWithOwner_(self, owner):
        '''
        Initializer to load from Nib.  Subclasses wishing to use a different Nib file can override
        (not overload) this method to initialize the `NSWindowController` (e.g. via
        `super.initWithWindowNibPath_owner_()`).  This method *must* return an initialized instance
        of the superclass.
        '''
        nibPath = _bundle_.pathForResource_ofType_(u'Toolglass', u'nib')
        self = super(ScottyToolglassWindowController, self).initWithWindowNibPath_owner_(nibPath, self)
        return self
    
    def awakeFromNib(self):
        self.window().setDelegate_(self)
    
    def windowWillClose_(self, notification):
        self.__instrument.deactivate()


ToolglassWindowController = ScottyToolglassWindowController

__all__ = 'ScottyToolglassWindowController ToolglassWindowController'.split()