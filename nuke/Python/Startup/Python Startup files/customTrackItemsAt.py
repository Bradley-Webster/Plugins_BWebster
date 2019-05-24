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
    
def subTrackItemsAt(sequence, frame):
    '''
    There is currently no "seq.subTrackItemsAt()" method, the following should work as an alternative.
    The method gets all VideoTracks, pulls out subTrackItems then checks if EffectTrack timeline range is within frame
    '''
    videoTracks = sequence.videoTracks()
    effectTrackList = []
    for track in videoTracks:
        subTrackItems = track.subTrackItems()
        for subTrackItem in subTrackItems:
            for effectTrack in subTrackItem:
                    timelineIn = effectTrack.timelineIn()
                    timelineOut = effectTrack.timelineOut()
                    effectRange = range(timelineIn,timelineOut)
    
                    # Check if the current frame is within Soft Effect timeline range
                    # If yes, add effectTrack to effectTrackList
                    if  frame in effectRange:
                        effectTrackList.append(effectTrack)

    # Return list of EffectTrack Objects
    return effectTrackList


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

    # Custom created definition, looks for Soft Effects at specific sequence and time
    effectTracks = subTrackItemsAt(seq, cv.time())

    for trackItem in timelineTrackItems:
        # Print any Video tracks to the Script Editor
        trackSource = trackItem.source()
        if trackSource != ():
            print 'Video Clip at Frame %s : %s ' % (cv.time(), trackSource.name())

    for effect in effectTracks:
        print 'Soft effect at Frame %s : %s ' % (cv.time(), effect.name())

    if timelineTrackItems == () and effectTracks == []:
        print 'No Video Clips or Effects found'

events.registerInterest("kPlaybackClipChanged", getCurrentTracksAndSubtracks)
