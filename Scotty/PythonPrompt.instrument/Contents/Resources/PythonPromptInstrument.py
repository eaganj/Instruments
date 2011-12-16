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
from PythonInterpreter import *

class PythonPromptInstrument(Instrument):
    # FIXME: Should the Python prompt functionality really be implemented as an Instrument?  It's a bit
    # different from the rest of the conception.
    
    name = u"Python Prompt"
    verb = u"Show Python prompt"
    
    def __init__(self):
        super(PythonPromptInstrument, self).__init__()
        self._initPrompt()
    
    def _initPrompt(self):
        self._interpreterController = None
    
    def activate(self, context=None):
        super(PythonPromptInstrument, self).activate(context)
        if not self._interpreterController:
            self._interpreterController = PythonInterpreterController.alloc().initWithInstrument_(self)
        self._interpreterController.showWindow_(self)
        # self.deactivate() # Immediately deactivate # FIXME:  should deactivate when window closes
    
    