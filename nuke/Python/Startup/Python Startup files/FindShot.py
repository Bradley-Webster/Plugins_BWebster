import hiero.core
import hiero.ui
import os
import re
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

def getAllTrackItems():
    """Collect all track items for current sequence (only to be run from inside the timeline editor)"""
    allTrackItems = []
    for track in hiero.ui.currentViewer().player().sequence():
        allTrackItems += [ti for ti in track]
    return allTrackItems


class ShotNameWidget(QtWidgets.QLineEdit):
    """Simple widget to type in shot names (track item names)"""
    selectedShotName = QtCore.Signal(str)

    def __init__(self, shotNameList=[]):
        super(ShotNameWidget, self).__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.shotNameList = sorted(shotNameList)
        self.setShotNames(self.shotNameList)
        self.returnPressed.connect(self.__emitShotName)

    def __emitShotName(self):
        self.selectedShotName.emit(self.text())
        self.close()

    def setShotNames(self, shotNameList):
        self.clear()
        self.shotNameList = sorted(shotNameList)
        completer = QtWidgets.QCompleter(self.shotNameList)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompleter(completer)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        super(ShotNameWidget, self).keyPressEvent(event)

    def showEvent(self, event):
        super(ShotNameWidget, self).showEvent(event)
        self.move(QtGui.QCursor.pos() - QtCore.QPoint(self.width() / 2, self.height() / 2))
        
class FindShotsInTimeline(QtWidgets.QAction):
    """Selects track items by shot name, kinda like in Nuke."""
    _zoomOutLevel = 25

    def __init__(self, name='Find Shots', parent=None):

        QtWidgets.QAction.__init__(self, name, parent)
        self.shotNameWidget = ShotNameWidget()
        self.triggered.connect(self.__getShotName)
        self.shotNameWidget.selectedShotName.connect(self.selectTrackItemsByShotName)
        hiero.core.events.registerInterest("kShowContextMenu/kTimeline", self.eventHandler)       

    def __getShotName(self):
        """provide the shot name the user is after"""

        self.activeView = hiero.ui.activeView()
        self.allTrackItems = getAllTrackItems()
        self.shotNameWidget.setShotNames(list(set([ti.name() for ti in self.allTrackItems])))
        self.shotNameWidget.show()

    def selectTrackItemsByShotName(self, shotName):
        """select the track items who's shot name match the requested shot name"""

        self.activeView.selectNone()
        newSelection = [trackItem for trackItem in self.allTrackItems if shotName in trackItem.name()]

        # select track items
        self.activeView.setSelection(newSelection)
        self.activeView.endSelectionUpdate()
        
        # adjust playhead
        firstFrameOfSelection = min([ti.timelineIn() for ti in newSelection])
        hiero.ui.currentViewer().setTime(firstFrameOfSelection)

        # zoom to fit
        fitAction = hiero.ui.findMenuAction('Zoom to Fit')
        fitAction.trigger()

        ## zoom out a few levels
        #zoomAction = hiero.ui.findMenuAction("Zoom Out")
        #for x in xrange(self._zoomOutLevel):
            #zoomAction.trigger()

    def eventHandler(self, event):
        # enable action to be registered into Hiero's default context menu
        event.menu.addAction(self)

        

findShotsAct = FindShotsInTimeline()
findShotsAct.setShortcut('/')
editMenu = hiero.ui.findMenuAction("Edit")
editMenu.menu().addAction(findShotsAct)
