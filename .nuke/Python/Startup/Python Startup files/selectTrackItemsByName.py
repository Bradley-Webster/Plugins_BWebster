import hiero.core, hiero.ui
from PySide2 import QtWidgets

class findTracksAction(QtWidgets.QAction):

    def __init__(self):
        QtWidgets.QAction.__init__(self, "Select Items Containing", None)
        self.setObjectName('Select_Items')
        self.triggered.connect(self.findTracksPanel)

    def findTracks(self, txt):
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
                        
    def findTracksPanel(self):
        txt = nuke.getInput('Select all track items containing:', 'new label')
        if txt:
            self.findTracks(txt)



Select_Items = findTracksAction()
hiero.ui.registerAction(Select_Items)

# Edit the following shortcut to your desired keyboard shortcut
Select_Items.setShortcut("/")

hiero.ui.insertMenuAction('foundry.menu.sequence', timeline_Edit_Menu)
