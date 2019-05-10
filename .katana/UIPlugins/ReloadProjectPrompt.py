"""
NAME: ReloadProjectPrompt
Bradley Webster - Foundry Customer Support

Reviews Recent Projects when starting Katana. 
If recent projects exist, ask if User would like to reload most recent.
"""
# Import Statements used for script
from Katana import (Callbacks, Configuration, KatanaPrefs, PrefNames, KatanaFile, UI4)
import os

# Qt Imports used for GUI popup, checks if user is on Katana3.1
from Katana import QtGui
try:
    from Katana import QtWidgets
except ImportError:
    QtWidgets = QtGui


# Check if Katana is launched in GUI mode
if Configuration.get('KATANA_UI_MODE'):

    def onStartupComplete(**kwargs):
        # Get the list of recent files from the preferences
        recentFiles = KatanaPrefs[PrefNames.RECENTFILES]
        if recentFiles:
            # Grab the first file from the list to use for the project.
            mostRecentFile = recentFiles.split(':SEPARATOR:', 1)[0].strip()
            if not os.path.isfile(mostRecentFile):
                return
                
            # Prompt the user to reload the project
            res = QtWidgets.QMessageBox.question(
                UI4.App.MainWindow.CurrentMainWindow(),
                "Load Recent Project", 
                "Recent project detected, would you like to reload it?\n\n"
                "Recent Project: %s" % mostRecentFile,
                buttons = QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                defaultButton=QtWidgets.QMessageBox.Yes)

            if res == QtWidgets.QMessageBox.Yes:
                print "Reloading scene: %s" % mostRecentFile
                KatanaFile.Load(mostRecentFile)

            elif res == QtWidgets.QMessageBox.No:
                return
                    
    # Adds function call on startup,  
    Callbacks.addCallback(Callbacks.Type.onStartupComplete, onStartupComplete)
