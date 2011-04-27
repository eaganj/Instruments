from Foundation import *
from AppKit import *
import objc

import ViewHierarchyClassBrowser

class ScottyViewHierarchyBrowserController(NSWindowController):
    browserDelegate = objc.IBOutlet()
    browser = objc.IBOutlet()
    widgetNameField = objc.IBOutlet()
    widgetFrameOriginXField = objc.IBOutlet()
    widgetFrameOriginYField = objc.IBOutlet()
    widgetFrameWidthField = objc.IBOutlet()
    widgetFrameHeightField = objc.IBOutlet()
    methodList = objc.IBOutlet()

    def initWithInstrument_(self, instrument):
        nibPath = instrument._bundle_.pathForResource_ofType_(u'ViewHierarchyBrowser', u'nib')
        self = super(ScottyViewHierarchyBrowserController, self).initWithWindowNibPath_owner_(nibPath, self)
        if not self:
            return self
        
        self._instrument = instrument
        
        return self

    def awakeFromNib(self):
        # NSString *bundlePath = [[NSBundle mainBundle] bundlePath];
        # NSString *appName = [[NSFileManager defaultManager] displayNameAtPath: bundlePath];
        appBundlePath = NSBundle.mainBundle().bundlePath()
        appName = NSFileManager.defaultManager().displayNameAtPath_(appBundlePath)
        # self.window().setTitle_(u"Browse Widget Hierarchy \u2014 %s" % (appName))
    
    @objc.IBAction
    def displaySelectedWidget_(self, sender):
        widget = sender.selectedCell().representedObject()
        frame = widget.frame()
        name = widget.__class__.__name__.replace('NSKVONotifying_', '')
        self.widgetNameField.setStringValue_(u"%s \u2014 (%s, %s), (%s x %s)" % (name, frame.origin.x, frame.origin.y, frame.size.width, frame.size.height))
        self.widgetFrameOriginXField.setStringValue_(frame.origin.x)
        self.widgetFrameOriginYField.setStringValue_(frame.origin.y)
        self.widgetFrameWidthField.setStringValue_(frame.size.width)
        self.widgetFrameHeightField.setStringValue_(frame.size.height)
        self.methodList.dataSource().reloadFromClass_(widget.__class__)
        self.methodList.reloadData()
        self._instrument.highlightWidget(widget)

ViewHierarchyBrowserController = ScottyViewHierarchyBrowserController

class ScottyViewHierarchyBrowserDelegate(NSObject):
    def init(self):
        self = super(ScottyViewHierarchyBrowserDelegate, self).init()
        if not self:
            return self
            
        self.columns = [ NSApp().allOrderedWindows() ]
        self.selected = None
        self.selectedClassMethods = []

        return self


    def browser_willDisplayCell_atRow_column_(self, browser, cell, row, col):
        if col == 0:
            cell.setLeaf_(len(self.columns[col][row].contentView().subviews()) <= 0)
        else:
            cell.setLeaf_(len(self.columns[col][row].subviews()) <= 0)

        cell.setStringValue_(self.columns[col][row].__class__.__name__.replace('NSKVONotifying_', ''))
        cell.setRepresentedObject_(self.columns[col][row])


    def browser_numberOfRowsInColumn_(self, browser, col):
        if col == 0:
            return len(self.columns[0])
        del self.columns[col:]
        if col == 1:
            subviews = self.columns[col - 1][browser.selectedRowInColumn_(col - 1)].contentView().subviews()
        else:
            subviews = self.columns[col - 1][browser.selectedRowInColumn_(col - 1)].subviews()
        self.columns.append(subviews)
        return len(subviews)
    
    def reloadFromClass_(self, cls):
        self.selectedClassMethods = dir(cls)

    # table view delegate methods
    def numberOfRowsInTableView_(self, tableView):
        if self.selectedClassMethods is None:
            return 0
        return len(self.selectedClassMethods)

    def tableView_objectValueForTableColumn_row_(self, tableView, col, row):
        return str(self.selectedClassMethods[row])

    def tableView_shouldEditTableColumn_row_(self, tableView, col, row):
        return 0
        
ViewHierarchyBrowserDelegate = ScottyViewHierarchyBrowserDelegate

__all__ = 'ViewHierarchyBrowserDelegate ScottyViewHierarchyBrowserDelegate '\
          'ViewHierarchyBrowserController ScottyViewHierarchyBrowserController'.split()

# >>> def subviews(view):
# ...   return [ view.__class__.__name__, ] + [ subviews(subview) for subview in view.subviews() ]