'''
Created By: FOUNDRY

The following Script is a workaround to the following issue:

TP 147048 - Linux - Support audio playback of movie file formats (QuickTime)

The workaround detects when an .MOV is dropped into the Timeline and creates a .WAV file for its audio track.
'''

import hiero.core
import nuke
from PySide2.QtCore import QTimer
from hiero.core.events import *
import os
import platform

class TilelineViewDropHandler:
  
  def __init__(self):
    # register interest in the drop event now
    registerInterest((EventType.kDrop, EventType.kTimeline), self.dropHandler)

  def dropHandler(self, event):
    try:
      # Handle clips dropped on the timeline and trigger replacing of audio in mov files. 
      # At this point the track items haven't been created yet, so need to use a single 
      # shot timer to wait until they have been
      track = event.track
      if isinstance(track, hiero.core.VideoTrack) and not hasattr(event, "trackItem"):
        binItems = event.items
        for binItem in binItems:
          clip = binItem.activeItem()
          filepath = clip.readNode().knob("file").value()
          if filepath.endswith(".mov") and clip.numAudioTracks() > 0:
            QTimer.singleShot(0, lambda: self.replaceAudio(binItem, track, filepath))
    except:
      import traceback
      traceback.print_exc()


  def extractAudio(self, clip):
    # Try to extract a wav file from the mov path using ffmpeg. Note this just
    # extracts the audio it doesn't re-encode it so will fail if the mov doesn't
    # contain wav data 
    filepath = clip.readNode().knob("file").value()
    
    audioFilepath = ('.').join(filepath.split('.')[:-1]) + ".wav"
    audioFilepathTemp = "/tmp/" + os.path.splitext(os.path.split(filepath)[1])[0] + ".wav"

    # Check if WAV already exists in Project file ( through audioFilepath ).
    # If the WAV does not exist, create it through an ffmpeg command. ( Linux ffmpeg program )
    if not os.path.exists(audioFilepath):
      ffmpegCommand = "ffmpeg -i %s -vn -acodec copy %s" % (filepath, audioFilepathTemp)
      if os.system(ffmpegCommand) != 0:
        raise RuntimeError("Running ffmpeg failed")
    return audioFilepath

  def replaceAudio(self, binItem, track, filepath):
    # Extract the audio
    clip = binItem.activeItem()
    audioFilepath = self.extractAudio(clip)
  
    # Create a new clip for the extracted audio file
    parentBin = binItem.parentBin()
    audioClip = parentBin.createClip(audioFilepath)

    # Find the video track item for the dropped clip (this assumes there is only one),
    # get the linked audio items, and set the wav as the source on them.
    trackItem = next(item for item in track if item.source() == clip)
    linkedAudioItems = trackItem.linkedItems()
    for audioItem in linkedAudioItems:
      audioItem.setSource(audioClip)

# Check if the OS is Linux, as issue does not occur on other platforms.
OS = platform.system()
if OS == 'Linux':
  # Instantiate the handler to get it to register itself.
  dropHandler = TilelineViewDropHandler()
    
