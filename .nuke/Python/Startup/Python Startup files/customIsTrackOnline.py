'''
Name: Custom subTrackItemsAt() Definition Testing
Version: 1.0
Created by: Bradley Webster - Foundry Customer Support Engineer

Description:
    Displays the Video and Effect tracks at a chosen time
    The chosen tracks are printed to the Script Editor
'''

import hiero.core , hiero.ui
from hiero.core import events
from PySide2 import QtCore
    

def getCurrentTracksAndSubtracks(event):
    '''
    Check current Timeline frame for Video and Soft Effect tracks
    Print any tracks at the position to the Scrit Editor
    '''
    seq = hiero.ui.activeSequence()
    cv = hiero.ui.currentViewer()
    videoTracks = seq.videoTracks()

    # Return enabled tracks at specified time from top to bottom, defaults to video
    timelineTrackItems = seq.trackItemsAt(cv.time()) 

    for trackItem in timelineTrackItems:
        # Print any Video tracks to the Script Editor
        trackSource = trackItem.source()
        trackMediaSource = trackItem.source().mediaSource()
        if trackSource != ():
            print 'Video Clip at Frame %s : %s ' % (cv.time(), trackSource.name())

        if trackMediaSource.isOffline():
            print 'Video Clip is offline'
        else:
            print 'Video Clip is offline'

events.registerInterest("kPlaybackClipChanged", getCurrentTracksAndSubtracks)
