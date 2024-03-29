"""ClassBrowser.py -- A simple class browser, demonstrating the use of an NSBrowser.

To build the demo program, run this line in Terminal.app:

    $ python setup.py py2app -A

This creates a directory "dist" containing ClassBrowser.app. (The
-A option causes the files to be symlinked to the .app bundle instead
of copied. This means you don't have to rebuild the app if you edit the
sources or nibs.)

See also the iClass demo.
"""

from PyObjCTools import AppHelper
from objc import getClassList, objc_object
from Foundation import *


try:
    import AddressBook
except ImportError:
    pass

try:
    import PreferencePanes
except ImportError:
    pass

try:
    import InterfaceBuilder
except ImportError:
    pass

def _sortClasses(classList):
    classes = [(cls.__name__, cls) for cls in classList]
    classes.sort()
    return [cls for name, cls in classes]


class ScottyViewHierarchyClassBrowserDelegate (NSObject):
    browser = objc.IBOutlet()
    pathLabel = objc.IBOutlet()
    table = objc.IBOutlet()

    selectedClassMethods = None

    def awakeFromNib(self):
        classes = getClassList()
        rootClasses = []
        for cls in classes:
            if cls.__base__ == objc_object:
                rootClasses.append(cls)
        rootClasses = _sortClasses(rootClasses)
        self.columns = [rootClasses]
        self.browser.setMaxVisibleColumns_(7)
        self.browser.setMinColumnWidth_(150)
        self.selectedClass = None
        self.selectedClassMethods = None

    def setRootClass_(self, cls):
        assert cls.__base__ == objc_object
        rootClasses = [cls]
        self.columns = [rootClasses]
        
    def browser_willDisplayCell_atRow_column_(self, browser, cell, row, col):
        cell.setLeaf_(not self.columns[col][row].__subclasses__())
        cell.setStringValue_(self.columns[col][row].__name__)

    def browser_numberOfRowsInColumn_(self, browser, col):
        if col == 0:
            return len(self.columns[0])
        del self.columns[col:]
        cls = self.columns[col - 1][browser.selectedRowInColumn_(col - 1)]
        subclasses = _sortClasses(cls.__subclasses__())
        self.columns.append(subclasses)
        return len(subclasses)

    @objc.IBAction
    def browserAction_(self, browser):
        self.pathLabel.setStringValue_(browser.path())

        self.selectedClass = None
        self.selectedClassMethods = None
        col = len(self.columns)
        row = -1
        while row == -1:
            col -= 1
            if col < 0:
                break
            row = self.browser.selectedRowInColumn_(col)
        if row >= 0:
            self.selectedClass = self.columns[col][row]
            # Classes get initialized lazily, upon the first attribute access,
            # only after that cls.__dict__ actually contains the methods.
            # Do a dummy hasattr() to make sure the class is initialized.
            hasattr(self.selectedClass, "alloc")
            self.selectedClassMethods = [
                '-' + obj.selector for obj in self.selectedClass.pyobjc_instanceMethods.__dict__.values()
                 if hasattr(obj, "selector")
            ]
            self.selectedClassMethods += [
                '+' + obj.selector for obj in self.selectedClass.pyobjc_classMethods.__dict__.values()
                if hasattr(obj, "selector")
            ]
            self.selectedClassMethods.sort()

        self.table.reloadData()

    # table view delegate methods
    def numberOfRowsInTableView_(self, tableView):
        if self.selectedClassMethods is None:
            return 0
        return len(self.selectedClassMethods)

    def tableView_objectValueForTableColumn_row_(self, tableView, col, row):
        return str(self.selectedClassMethods[row])

    def tableView_shouldEditTableColumn_row_(self, tableView, col, row):
        return 0

if __name__ == "__main__":
    AppHelper.runEventLoop()
