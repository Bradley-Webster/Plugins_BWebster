import hiero.core
import hiero.ui
from hiero.ui import findMenuAction, insertMenuAction, createMenuAction

# Set up PySide, create exception for PySide2 (for Nuke11+ scripts)
try:
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


# CustomContextMenuTest Class for Menu and actions
class CustomContextMenuTest:
    """This Class creates 4 menu actions"""
    # This constants drive the menu actions
    Menu_1 = "Menu 1"
    Menu_2 = "Menu 2"
    Menu_3 = "Menu 3"
    Menu_4 = "Menu 4"

    def __init__(self):
        # Menu Name
        self._menu = QMenu("Custom Context Menu")
        # Menu Icon (Optional)
        self._menu.setIcon(QIcon("icons:TagSnow.png"))

        # Create the menu items (Replace 'self.TestMenuItem' with your function)
        self._Sub_Menu_1 = createMenuAction(self.Menu_1, self.TestMenuItem)
        self._Sub_Menu_2 = createMenuAction(self.Menu_2, self.TestMenuItem)
        self._Sub_Menu_3 = createMenuAction(self.Menu_3, self.TestMenuItem)
        self._Sub_Menu_4 = createMenuAction(self.Menu_4, self.TestMenuItem)

        # Give the menu items keyboard shortcuts
        #self._Sub_Menu_1.setShortcut('<Double-1>')
        self._Sub_Menu_1.setShortcut(QtGui.QKeySequence('ctrl+1'))
        self._Sub_Menu_2.setShortcut(QtGui.QKeySequence('ctrl+2'))
        self._Sub_Menu_3.setShortcut(QtGui.QKeySequence('ctrl+3'))
        self._Sub_Menu_4.setShortcut(QtGui.QKeySequence('ctrl+4'))

        # Add actions to the QMenu
        self._menu.addAction(self._Sub_Menu_1)
        self._menu.addAction(self._Sub_Menu_2)
        self._menu.addAction(self._Sub_Menu_3)
        self._menu.addAction(self._Sub_Menu_4)

        # Add keyboard shortcut
        hiero.ui.mainWindow().addAction(self._Sub_Menu_1)
        hiero.ui.mainWindow().addAction(self._Sub_Menu_2)
        hiero.ui.mainWindow().addAction(self._Sub_Menu_3)
        hiero.ui.mainWindow().addAction(self._Sub_Menu_4)

        # Register for Timeline View and Viewer right-click menus
        hiero.core.events.registerInterest("kShowContextMenu/kTimeline", self.timelineEventHandler)

    ##### Context menu Handlers #####
    def timelineEventHandler(self, event):
        insertMenuAction(self._menu.menuAction(), event.menu)

    ##### TEST FUNCTION (Replace with your desired function) #####
    def TestMenuItem(instance):
        print 'Test Menu Item initiated'

# Call and create the custom context menu
act = CustomContextMenuTest()
menu = act._menu

# Add to Timeline Menu so that shortcuts work
hiero.ui.addMenuAction("foundry.menu.timeline", menu.menuAction())
