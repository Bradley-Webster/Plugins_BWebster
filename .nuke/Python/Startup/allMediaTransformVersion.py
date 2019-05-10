import hiero.core, hiero.ui
from PySide2 import QtWidgets
from hiero.core import events

class copyMediaTransform(QtWidgets.QAction):

    def __init__(self, event): 
        QtWidgets.QAction.__init__(self, "", None) 
        self.event = event
        self.triggered.connect(self.doit)

    def doit(self):
        if self.event.sender.getSelection():
            for binItem in self.event.sender.selection():
                colourSpace = binItem.activeItem().sourceMediaColourTransform()
                for version in binItem.items():
                    version.item().setSourceMediaColourTransform(colourSpace)

def AddActionToMenu(event):
    menu = event.menu
    menu.addAction("Copy Media Color Transform to All Clip Versions", lambda: copyMediaTransform(event).trigger())

events.registerInterest((events.EventType.kShowContextMenu, events.EventType.kBin), AddActionToMenu)
