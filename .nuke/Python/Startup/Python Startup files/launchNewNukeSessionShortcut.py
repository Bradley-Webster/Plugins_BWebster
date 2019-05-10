import hiero.core, hiero.ui
from PySide2 import QtWidgets

"""
This script was created in response to Ticket 33833

The following script is used to open a new Nuke window from a selected timeline clip.

When the keyboard shortcut is pressed while selecting the clip, a new Nuke window will launch
and Hiero's script editor will print a statement where the file is being opened from.
"""

class OpenCompAction(QtWidgets.QAction):

    def __init__(self):
        QtWidgets.QAction.__init__(self, "Open Comp", None)
        self.setObjectName('open_comp')
        self.triggered.connect(self.doit)

    def doit(self):
        nukeFile = False
        selection = hiero.ui.getTimelineEditor(hiero.ui.activeSequence()).selection()
        for item in selection:
            filePath = item.source().mediaSource().firstpath()
            if filePath.endswith(".nk"):
                nukeFile = True
                print "Opening in New Nuke Session: " + str(filePath)
                hiero.core.nuke.Script.launchNuke(filePath)
        if nukeFile == False:
            print "No Nuke Script('nk') file selected."

open_comp = OpenCompAction()
hiero.ui.registerAction(open_comp)

# Edit the following shortcut to your desired keyboard shortcut
open_comp.setShortcut("/")

hiero.ui.mainWindow().addAction(open_comp)
