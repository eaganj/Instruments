from __future__ import with_statement

from StateMachines import *

from IIKit import *

from SMTestGlassView import *

class SMTestInstrument(SMInstrument):
    name = u"State Machine Tester 2" # FIXME refactor
    verb = u"Test state machine 2"
    
    def __init__(self):
        super(SMTestInstrument, self).__init__()
        
        
        self.colors = [NSColor.redColor(), NSColor.blueColor(), NSColor.greenColor()]
        self.colorIndex = -1
        self.glassView = None
    
    def wantsGlassWindow(self):
        return True
        
    def newGlassViewForGlassWindow(self, glassWindow):
        window = glassWindow.parentWindow()
        view = SMTestGlassView(window.frame(), self)
        return view
    
    def shouldHijackInteraction(self):
        return True
    
    @state
    def start(self):
        @transition(LeftMouseDown, to=self.drawing)
        def action(event):
            self.glassView = InstrumentManager.sharedInstrumentManager().glassViewForWindow(event.window())
            self.colorIndex = (self.colorIndex + 1) % len(self.colors)
            color = self.colors[self.colorIndex]
            self.glassView.addPathWithColor_(color)

    @state
    def drawing(self):
        def enter():
            assert self.glassView is not None
            
        @transition(LeftMouseUp, to=self.start)
        def action(event):
            pass

        @transition(LeftMouseDragged)
        def action(event):
            self.glassView.addDrawPoint_(event.locationInWindow())
        
        def leave():
            self.glassView = None

