import hiero.core , hiero.ui
import nuke
from hiero.core import events
from PySide2 import QtCore
    
def showCurrentTracksInPropertiesBin():

    includeClips = 1
    includeEffects = 1

    seq = hiero.ui.activeSequence()
 
    # Getting 'current' item
    cv = hiero.ui.currentViewer()
    # Return enabled tracks at specified time from top to bottom, defaults to video
    timelineTrackItems = seq.trackItemsAt(cv.time()) 

    # You can reverse the order by editing the for loop to  "for trackItem in reversed(timelineTrackItems):"
    for trackItem in timelineTrackItems:
 
        # Display all track clip nodes in Properties bin (Can be disabled when calling definition)
        if includeClips == 1:
            trackSource = trackItem.source()
            nuke.show(trackSource.readNode())
 
        # Display all effect nodes in the Properties bin (Can be disabled when calling definition)
        if includeEffects == 1:
            subTracks = trackItem.parent().subTrackItems()[0]
            for effectTrack in subTracks:
                effectIn = effectTrack.timelineIn()
                effectOut = effectTrack.timelineOut()
                # get effect items at current time only
                if effectIn <= cv.time() <= effectOut:
                    effectNode = effectTrack.node()
                    # display effect nodes in Properties bin
                    nuke.show(effectNode)


def hideNodesFromPropertiesBin():
    
    seq = hiero.ui.activeSequence()

    videoTracks = seq.videoTracks()

    for track in videoTracks:

        # Remove all clips from properties bin
        trackItems = track.items()
        for trackItem in trackItems:
            trackSource = trackItem.source()
            print 'Hid clip properties: ', trackSource.readNode().name()
            trackSource.readNode().hideControlPanel()

        # Remove all effect tracks from properties bin
        subTracks = track.subTrackItems()
        subTracks = trackItem.parent().subTrackItems()[0]
        for effectTrack in subTracks:
            effectNode = effectTrack.node()
            print 'Hid effect properties: ', effectNode.name()
            effectNode.hideControlPanel() 

def dynamicPropertiesBin(event):

    hideNodesFromPropertiesBin()

    # Tiny delay rebuild to allow removal of current nodes
    QtCore.QTimer.singleShot(20, showCurrentTracksInPropertiesBin)

def registerDynamicBin():
    events.registerInterest("kPlaybackClipChanged", dynamicPropertiesBin)
    print "Dynamic Properties Bin enabled"

def unregisterDynamicBin():
    events.unregisterInterest("kPlaybackClipChanged", dynamicPropertiesBin)
    print "Dynamic Properties Bin disabled"  

