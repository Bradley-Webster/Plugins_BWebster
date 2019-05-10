'''
Created by: Bradley Webster - FOUNDRY SUPPORT ENGINEER

Description: A new MENU and ACTION is added to the Project Bin custom context menu.
             When the ACTION is initiated, it will ADD or REFRESH the SYNC folder with added items.
'''

# Import Hiero statements
from hiero.core import *
from hiero.ui import *

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

# Set the Following Variable for your SYNC folder location
FOLDERPATH = 'E:\Users\PC_SYD_PC2_E_Drive\Pictures\Test_Footage\SYNC_FolderTest'


# CustomContextMenu Class for Menu and actions
class CustomContextMenu:
    # This constants drive the menu actions
    Menu_1 = "SYNC Test Folder"

    def __init__(self):
        # Menu Name
        self._menu = QMenu("Custom Context Menu")
        # Menu Icon (Optional)
        self._menu.setIcon(QIcon("icons:TagSnow.png"))

        # Create the menu items (Replace 'self.TestMenuItem' with your function)
        self._Sub_Menu_1 = createMenuAction(self.Menu_1, self.SYNCFolderEvent)

        # Give the menu items keyboard shortcuts
        self._Sub_Menu_1.setShortcut(QtGui.QKeySequence('ctrl+1'))

        # Add actions to the QMenu
        self._menu.addAction(self._Sub_Menu_1)

        # Add keyboard shortcut
        hiero.ui.mainWindow().addAction(self._Sub_Menu_1)

        # Register for Project View and Viewer right-click menus
        hiero.core.events.registerInterest("kShowContextMenu/kBin", self.timelineEventHandler)

    ##### Context menu Handlers #####
    def timelineEventHandler(self, event):
        insertMenuAction(self._menu.menuAction(), event.menu)

    def SYNCFolderEvent(self):
      thisProject = projects()[-1]
      clipsBin = thisProject.clipsBin()

      testPATH = self.findBinNameInProject()

      print testPATH

      try:
        newBin = clipsBin.importFolder(FOLDERPATH)
        if str(newBin) != "Bin('None')":
          self.collateDupeBins(clipsBin, newBin)
        print "Sync Complete"
      except:
        print 'Sync Failed.'


    def findBinNameInProject(self):
      # Get BinView
      activeView = hiero.ui.activeView()

      # Get Selection
      currentSelection = activeView.selection()

      # Use first selected item name
      binName = currentSelection[0].name()

      ### USE binName as the folder name and use it to find the path within your database ###


      FOLDERPATH = 'C:/Path/To/Sequence/Shot/' + binName

      return FOLDERPATH


    def collateDupeBins(self, clipsBin, newBin):
      ''' Checks if Clips bin has duplicate names, merges bin items and removes new bin '''
      for syncBin in clipsBin.bins():
        # Make sure the syncBin does not equal itslf  (We are looking for older bins)
        if syncBin != newBin:
          # Check if the syncBin has the same name as the newBin
          if syncBin.name() == newBin.name():
            # Collate the newBin items and add them to the original bin
            newBinItems = newBin.items()
            for item in newBinItems:
              syncBin.addItem(item)

            # Remove the newBin after collating the new items
            clipsBin.removeItem(newBin)


# Call and create the custom context menu
act = CustomContextMenu()
menu = act._menu

# Add to Timeline Menu so that shortcuts work
hiero.ui.addMenuAction("foundry.menu.bin", menu.menuAction())