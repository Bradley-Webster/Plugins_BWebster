import hiero.core
import hiero.ui
import nuke
from functools import partial

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


# select_Tracks_Containing Class for Menu and actions
class select_Tracks_Containing(object):

    def __init__(self):
        hiero.core.events.registerInterest('kShowContextMenu/kTimeline', self.event_handler)

    def event_handler(self, event):
        self._selection = event.sender.selection()

        if len(self._selection) > 0:
            self._action = QAction('Select Tracks Containing', None)
            self._action.triggered.connect(self.findTracks)
            # User must right click timeline once to add the action.
            for action in event.menu.actions():
                if str(action.text()) == 'Editorial':
                    # Add action UI
                    action.menu().addAction(self._action)
                    # Add keyboard shortcut
                    self._action.setShortcut('/')
                    hiero.ui.mainWindow().addAction(self._action)
                    break


    def findTracks(self):
        txt = nuke.getInput('Select all track items containing:', 'new label')
        if txt:
            seq = hiero.ui.activeSequence()
            timelineTracks = seq.items()
            timelineEditor = hiero.ui.getTimelineEditor(seq) 

            matchingItems = []
            for timelineTrackItems in timelineTracks:
                for trackItem in timelineTrackItems:
                    if txt.lower() in trackItem.source().name().lower():
                        if isinstance(trackItem, hiero.core.TrackItem):
                            matchingItems.append(trackItem)
                
            timelineEditor.setSelection(matchingItems)

select_Tracks_Containing()
