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
        self.deactivate() # Immediately deactivate # FIXME:  should deactivate when window closes
    
    