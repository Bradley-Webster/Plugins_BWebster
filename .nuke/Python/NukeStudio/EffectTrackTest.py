from hiero.core import TrackItem
from hiero.core import EffectTrackItem

currentSequence = hiero.ui.activeSequence()

currentTimeline = hiero.ui.getTimelineEditor(currentSequence)


currentSelection = currentTimeline.selection()

print currentSelection


cv = hiero.ui.currentViewer()
setTest = currentSequence.trackItemAt(cv.time())

print setTest

effectTest = setTest.parent()

print effectTest

gradeSubTrack = effectTest.subTrackItems()

print gradeSubTrack

trackItemName = 'testGrade'
# Handle SubTrackItems on Video Tracks
if isinstance(track, hiero.core.VideoTrack):
    subTracks = track.subTrackItems()
    for subTrack in subTracks:
        for subTrackItem in subTrack:
              if subTrackItem.name() == trackItemName:
                print '\n Found Effect track', subTrackItem.name



