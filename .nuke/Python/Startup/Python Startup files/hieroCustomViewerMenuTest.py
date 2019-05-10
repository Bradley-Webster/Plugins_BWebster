
# Set up PySide, create exception for PySide2 (for Nuke11+ scripts)
try:
    from PySide import QtGui, QtCore

except ImportError:
    from PySide2 import QtCore, QtGui
    from PySide2 import QtWidgets

# CustomContextMenuTest Class for Menu and actions
class CustomContextMenuTest:
    """This Class creates 1 menu action, more can by added cia copying the init values below"""
    # This constants drive the menu actions
    Menu_1 = "Print Test"

    def __init__(self):
        # Menu Name
        self._menu = QtWidgets.QMenu("Custom Context Menu")
        # Menu Icon (Optional)
        self._menu.setIcon(QtGui.QIcon("icons:TagSnow.png"))

        # Create the menu items (Replace 'self.TestMenuItem' with your function)
        self._Sub_Menu_1 = hiero.ui.createMenuAction(self.Menu_1, self.TestMenuItem)

        self._Sub_Menu_1.setShortcut(QtGui.QKeySequence('/'))

        # Add actions to the QMenu
        self._menu.addAction(self._Sub_Menu_1)

        # Add keyboard shortcut
        hiero.ui.mainWindow().addAction(self._Sub_Menu_1)

        # Register for Timeline View and Viewer right-click menus
        hiero.core.events.registerInterest("kShowContextMenu/kViewer", self.viewerEventHandler)

    ##### Context menu Handlers #####
    def viewerEventHandler(self, event):
        hiero.ui.insertMenuAction(self._menu.menuAction(), event.menu)

    ##### TEST FUNCTION (Replace with your desired function) #####
    def TestMenuItem(instance):
        print 'Test Menu Item initiated'

# Call and create the custom context menu
act = CustomContextMenuTest()
menu = act._menu

# Add to Timeline Menu so that shortcuts work
hiero.ui.addMenuAction("foundry.menu.viewer", menu.menuAction())




