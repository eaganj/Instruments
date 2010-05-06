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