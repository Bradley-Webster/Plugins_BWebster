
from hiero.ui import *
from hiero.core import *
import PyOpenColorIO as OCIO
import math
import sys
import os
import bb_python.Workspace as bbw
import getWorkspaceEnv as getws
from PySide2 import QtGui, QtCore
from hiero.ui.BuildExternalMediaTrack import *
from hiero.ui.nuke_bridge.send_to_nuke import *
from hiero.ui.nuke_bridge.hiero_state import *
import re
import ast
import traceback


def getFirstTrackItem(trackName):
  track = getTrackByName(trackName)
  name = track.name()
  FirstTrackItem = track.items()[0]
  return FirstTrackItem


# Quickly get a  getLastTrackItem('Comp')
def getLastTrackItem(trackName):

  track = getTrackByName(trackName)
  name = track.name()
  LastTrackItem = track.items()[-1]
  return LastTrackItem


# ADD A TESTFILE TO THE TEST BIN
def getTestFilesIntoComp():
  project = myProject
  track = getTrackByName2(myProject, 'Comp')
  source = MediaSource('/shows/nysm2/shots/wh/wh_147_0100/publish/comp/output/v006/dpx/2048x1536/wh_147_0100_logc_v006.%04d.dpx')
  #source = MediaSource('/disk1/ski_community/CM_snow_countdown_selects/CM_Snow_Countdown_skiing.mov')
  # source = MediaSource('/Volumes/disk1/dpx/002_mmh_0074/publish/plate/input_plate/bg01/v001/dpx/2048x1152/002_mmh_0074_bg01_logc_v001.####.dpx')
  testclip = Clip(source)
  sequence = project.sequences()[0]  # sequence = hiero.ui.activeSequence() relies on
  clipsBin = sequence.project().clipsBin()
  bin = Bin("Testing")
  clipsBin.addItem(bin)
  bin.addItem(BinItem(testclip))
  #createTrackItem2(track, "test", testclip, lastTrackItem=None, timeIn=None)
  createTrackItem(track, "test", testclip, lastTrackItem=None, timeIn=None)
  # testclip.refresh() #no longer needed


def getTrackByName(name):
  sequence = hiero.ui.activeSequence()
  for tr in sequence.videoTracks():
    if tr.name() == name:
      targetTrack = tr
  return targetTrack


# Need to replace getTrackByName with getTrackByName2 in other parts of the script.
def getTrackByName2(project, trackName):
  project = myProject

  targetTrack = None

  if project.sequences():
    sequence = project.sequences()[0]
    for track in sequence.videoTracks():
      if track.name() == trackName:
        targetTrack = track

  return targetTrack


#  should really be using VideoTrack's addTrackItem(clip, position), which creates and returns a TrackItem
#  addItem is marked as deprecated:  doesn't cause timeline editor and Viewer to auto-update.
#  TrackBase.items() returns the items ordered by their position along the track so don't need to search
#  for one with highest timeout

def createTrackItem(track, trackItemName, sourceClip, lastTrackItem=None, timeIn=None):

  if lastTrackItem:
    timeIn = lastTrackItem.timelineOut() + 1
  elif timeIn == None:
    trackItems = track.items()
    if trackItems:
      lastTrackItem = trackItems[len(trackItems) - 1]
      timeIn = lastTrackItem.timelineOut() + 1
    else:
      timeIn = 0

  trackItem = track.addTrackItem(sourceClip, timeIn)

  trackItem.setName(trackItemName)

  return trackItem


def createTrackItem1(track, trackItemName, sourceClip, lastTrackItem=None):
  # create the track item
  trackItem = track.createTrackItem(trackItemName)

  # set it's source
  trackItem.setSource(sourceClip)

  # set it's timeline in and timeline out values, offseting by the track item before if need be
  if lastTrackItem:
    trackItem.setTimelineIn(lastTrackItem.timelineOut() + 1)
    trackItem.setTimelineOut(lastTrackItem.timelineOut() + sourceClip.duration())
  else:
    trackItem.setTimelineIn(0)
    trackItem.setTimelineOut(trackItem.sourceDuration() - 1)

  # add the item to the track
  track.addItem(trackItem)
  trackItem.setEnabled(False)
  trackItem.setEnabled(True)
  return trackItem


def createTrackItem2(track, trackItemName, sourceClip, lastTrackItem=None, timeIn=None):
    # create the track item

  trackItem = track.createTrackItem(trackItemName)

  if timeIn == None:
    last = -1
    for it in track.items():
      if it.timelineOut() > last:
        last = it.timelineOut()
    timeIn = last

  trackItem.setSource(sourceClip)

  trackItem.setTimelineIn(timeIn + 1)
  trackItem.setTimelineOut(timeIn + sourceClip.duration())

  track.addItem(trackItem)

  return trackItem


def findResourcePath():
  hieroExecutablePath = QtCore.QCoreApplication.applicationDirPath()
  resourcesPath = str(os.path.abspath(os.path.join(hieroExecutablePath, "Documentation", "Python", "Resources")))

  # OS X paths are a bit different...
  if sys.platform.startswith("darwin"):
    hieroExecutablePath = os.path.join(hieroExecutablePath, "..")
    resourcesPath = str(os.path.abspath(os.path.join(hieroExecutablePath, "Resources", "Python", "Resources")))

  return resourcesPath


def createProject():
  # find the path to the resources that ship with Hiero
  resourcesPath = findResourcePath()

  #################################
  # create a new project and Bins
  #################################
  # create a new project
  global myProject
  myProject = newProject()

  # create some bins for it
  bin1 = Bin("Sequences")
  bin2 = Bin("Shots")
  bin3 = Bin("Cut Refs")
  bin4 = Bin("Audio")

  # make bin2 a sub bin of bin1
  # bin1.addItem(bin2)

  # attach the bins to the project
  clipsBin = myProject.clipsBin()
  clipsBin.addItem(bin1)
  clipsBin.addItem(bin2)
  clipsBin.addItem(bin3)
  clipsBin.addItem(bin4)

  #################################
  # Add Media to the clips
  #################################

  # create a new sequence and attach it to the project and set its framerate
  global sequence
  sequence = Sequence("NewSequence")

  fps = os.getenv('FPS')
  if fps is None:
    print "Unknown FPS"
    fps = 24.0

  sequence.setFramerate(fps)
  clipsBin.addItem(BinItem(sequence))

  # helper method for creating track items from clips

  # create a track to add items/clips to
  track = VideoTrack("Comp")

  # create the track items, each one offset from the one before it
  #trackItem1 = createTrackItem2(track, "TrackItem1", clip1)
  #trackItem2 = createTrackItem2(track, "TrackItem2", clip2, lastTrackItem=trackItem1)

  # add the track to the sequence now
  sequence.addTrack(track)

  ##########################################
  # Add the Tranform Effects then the Text
  #########################################

  addInfoStrip(sequence)

  return myProject


def addTopLeftInfoStrip(sequence=None):
  addInfoStrip(sequence=sequence, corner="topLeft")


def addBottomLeftInfoStrip(sequence=None):
  addInfoStrip(sequence=sequence, corner="bottomLeft")


def addInfoStrip(sequence=None, corner="topLeft"):
  # find the path to the resources that ship with Hiero
  resourcesPath = findResourcePath()

  #################################
  # Find Current Sequence
  #################################
  # create a new project
  if sequence is None:
    sequence = hiero.ui.activeSequence()

  moveInfoStripExpressionT = '''
[python -exec {
from hiero.ui import *
from hiero.core import *

sequence = hiero.ui.activeSequence()


fromTop=15

ret=sequence.format().height()-fromTop
} ]

[python ret]
'''

  strip_name = "Top Info Strip"
  if corner == "bottomLeft":
    strip_name = "Bottom Info Strip"

  for track in sequence.videoTracks():
    if track.name().endswith("Info Strip"):
      sequence.removeTrack(track)
      if track.name() == strip_name:
        return

  track = VideoTrack(strip_name)

  sequence.addTrack(track)

  # textEffect = EffectTrackItem("Text2", timelineIn=1, timelineOut=20000)
  # track.addSubTrackItem(textEffect, 0)

  textEffect = track.createEffect("Text2")

  n = textEffect.node()
  n.knob("font_size").setValue(25)

  n.knob("box").setY(15)
  n.knob("box").setR(4000)
  n.knob("box").setX(15)
  n.knob("box").setT(sequence.format().height() - 15)
  n.knob("enable_background").setValue(True)
  n.knob("background_color").setValue(0)

  n.knob("box").setExpression(moveInfoStripExpressionT, 3)
  n.knob("font").setValue("DejaVu Sans Mono", "Book")

  message = """[python -exec {
filename=hiero.ui.activeSequence().trackItemAt(hiero.ui.currentViewer().time()).source().mediaSource().filename()
splits=filename.split(".")
ext=splits[-1]
if len(splits)>2:
  ret = '.'.join(splits[:-2])
else:
  ret = '.'.join(splits[:-2])
}][python ret] [python hiero.ui.activeSequence().trackItemAt(hiero.ui.currentViewer().time()).source().mediaSource().metadata().dict().get(\"foundry.source.width\")] x [python hiero.ui.activeSequence().trackItemAt(hiero.ui.currentViewer().time()).source().mediaSource().metadata().dict().get(\"foundry.source.height\")] [python hiero.ui.activeSequence().trackItemAt(hiero.ui.currentViewer().time()).source().mediaSource().metadata().dict().get(\"foundry.source.pixelAspectRatio\")] - [metadata input/frame_rate]fps - [metadata input/frame]"""
  n.knob("message").setValue(message)

  # k=n['font_size_values']
  constantSizeFunc = '''
[python -exec {
from hiero.ui import *
from hiero.core import *

sequence = hiero.ui.activeSequence()
ret=(((0.03/400.0)*sequence.format().width()*sequence.format().pixelAspect())+.01)
if ret<0.12: ret = 0.12
} ]

[python ret]
  '''
  n.knob("global_font_scale").setExpression(constantSizeFunc)
  if corner == "topLeft":
    n.knob("xjustify").setValue("left")
    n.knob("yjustify").setValue("top")
  elif corner == "bottomLeft":
    n.knob("xjustify").setValue("left")
    n.knob("yjustify").setValue("bottom")

  textEffect2 = track.createEffect("Text2")
  n = textEffect2.node()
  n.knob("font_size").setValue(25)
  n.knob("box").setY(15)
  n.knob("box").setR(4000)
  n.knob("box").setX(15)
  n.knob("box").setT(sequence.format().height() - 15)
  n.knob("enable_background").setValue(False)
  n.knob("box").setExpression(moveInfoStripExpressionT, 3)
  n.knob("font").setValue("DejaVu Sans Mono", "Bold")
  bold_version_number_message = """[python -exec {
filename=hiero.ui.activeSequence().trackItemAt(hiero.ui.currentViewer().time()).source().mediaSource().filename()
splits=filename.split(".")
ext=splits[-1]
if len(splits)>2:
  filename = '.'.join(splits[:-2])
else:
  filename = '.'.join(splits[:-2])
import re
matches = re.search('v[0-9]+',filename)
if matches:
  first_instance = matches.group(0)
  first_index = filename.find(first_instance,0)
  ret=" "*(first_index) + first_instance
else:
  ret=""
}][python ret]"""

  n.knob("message").setValue(bold_version_number_message)
  n.knob("global_font_scale").setExpression(constantSizeFunc)

  if corner == "topLeft":
    n.knob("xjustify").setValue("left")
    n.knob("yjustify").setValue("top")
  elif corner == "bottomLeft":
    n.knob("xjustify").setValue("left")
    n.knob("yjustify").setValue("bottom")


def getAllBinClips(thisBin):
  clipList = []
  allClips = thisBin.clips()
  for clip in allClips:
    clipList.append(clip)
  allBins = thisBin.bins()
  for newBin in allBins:
    clipList = clipList + getAllClips(newBin)
  return clipList


def getAllTrackClips(trackName):
  track = getTrackByName(trackName)
  clipList = []
  allClips = track.items()
  for clip in allClips:
    clipList.append(clip)
  return clipList


def getColourSpaceNameFromTrackItem(ti):
  config = OCIO.GetCurrentConfig()
  colourSpace = config.parseColorSpaceFromString(ti.source().name())
  print "=================================="
  print colourSpace
  print "=================================="
  if colourSpace == "logc":
    colourSpace = "arri/logc"  # Bug where it returns log if logc
  if colourSpace == "slog3":
    colourSpace = "sony/slog3"  # Bug where it returns log if logc
  return colourSpace


def setTrackItemSourceColourbyName(ti):
  colourSpace = getColourSpaceNameFromTrackItem(ti)
  if colourSpace == "arri/logc":  # Bug where it returns log if logc, but mediacolourtranform does not accept arr/logc
    colourSpace = "logc"
  if colourSpace == "sony/slog3":
    colourSpace = "slog3"
  ti.setSourceMediaColourTransform(colourSpace)


def trunc_at(s, d, n=3):
  "Returns s truncated at the n'th (3rd by default) occurrence of the delimiter, d."
  return d.join(s.split(d)[:n])


def rev_trunc_at(s, d, n=2):
  "Trying to reverse above - but fails"
  return d.join(s.split(d)[n:])


# Set a different working
def addOcioFileTransformEffectsToTrackItem(trackItem, track, effect, sourceFilePath, extension, fallbackFile=None, fallbackFileLabel=None, workingSpace=None, subTrackIndex=0):

  effect1 = track.createEffect(effectType=effect, trackItem=trackItem, subTrackIndex=subTrackIndex)
  workingSpace = getColourSpaceNameFromTrackItem(trackItem)
  effect1.node()['working_space'].setValue(workingSpace)
  shotName = trunc_at(trackItem.source().name(), "_", 3)
  if sourceFilePath:
    sourceFile = sourceFilePath + shotName + "." + extension
    if os.path.exists(sourceFile):
      effect1.setName(shotName + "_" + extension)
      effect1.node()['file'].setValue(sourceFile)
    else:
      #fallbackName = rev_trunc_at(fallbackFile,"/",6)
      if fallbackFileLabel:
        effect1.setName(fallbackFileLabel)
      effect1.node()['file'].setValue(fallbackFile)


def addOcioColourSpaceToTrackItem(trackItem, track, targetSpace=None, sourceSpace=None):
  effect1 = track.createEffect(effectType="OCIOColorSpace", trackItem=trackItem, subTrackIndex=0)
  # if not targetSpace:
  #   targetSpace = getColourSpaceNameFromTrackItem(trackItem)
  # effect1.node()['out_colorspace'].setValue(targetSpace)
  # if not sourceSpace:
  #   effect1.node()['in_colorspace'].setValue("lnf")


def setupColourTransformTrackByName(trackName):
  track = getTrackByName2(myProject, trackName)
  name = track.name()
  clipList = []
  clipList = getAllTrackClips(name)
  for clip in clipList:
    colourspaceEffect = track.createEffect(effectType="OCIOColorSpace", trackItem=clip)
    clipName = clip.source().name()
    shotName = trunc_at(clipName, "_", 3)
    config = OCIO.GetCurrentConfig()
    colorSpaceName = config.parseColorSpaceFromString(clip.name())
    colourspaceEffect.setName(shotName + "delin")
    colourspaceEffect.node()['out_colorspace'].setValue("arri/logc")


def setupColourForTrack_old(trackName):
  track = getTrackByName2(myProject, trackName)
  for item in track.items():
    if not item.linkedItems():
      setTrackItemSourceColourbyName(item)
      addOcioFileTransformEffectsToTrackItem(item, track, "OCIOFileTransform", os.environ['OCIO_PATH'] + "/looks/", "cc", "/shows/bluebolt/tools/ocio/looks/None.cc")
      addOcioFileTransformEffectsToTrackItem(item, track, "OCIOFileTransform", os.environ['OCIO_PATH'] + "/luts/", "cube", os.environ['OCIO_PATH'] + "/luts/client.cube", "client_cube")
    addOcioColourSpaceToTrackItem(item, track, targetSpace=None, sourceSpace=None)


# Not sure if this is a bug or  I'm not understanding subtracks correctly.
# Doing all effects to one clip, then moving to the next clip and applying effect is probably better but causes
# An unsightly cascading effect in the subtrackitems.
# To get around this I add each effect to every clip (on a single subtrack) then move to the next subtrack
# This works when there are no subtrack items - however the moment you have some subtrack items the
# Issue arises again.
# To get around these I replace all of the clips in the track and start from scratch.
# This does not fully solve the issue but means that all of the subtracks are not cascading but
# equally wrong. The more times you do this the higher the subtrackitems get.
# I did discover that removing a subtrack item from any clip fixes this issue
# So I create a duplicate trackitem at the end and remove the last subtrackitem on the track,
# which will be attached to it. Kills the clip and fixes the timeline. Kill me!

def setupColourForTrack(trackName):
  track = getTrackByName(trackName)
  for item in track.items():
    tli = item.timelineIn()
    ts = item.source()
    createTrackItem(track, item.source().name(), ts, None, tli)
  # create a duplicate dummy track item for last one so we can remove it.
  createTrackItem(track, item.source().name(), ts)
  for item in track.items():
    setTrackItemSourceColourbyName(item)
  for item in track.items():
    addOcioFileTransformEffectsToTrackItem(item, track, "OCIOFileTransform", os.environ['OCIO_PATH'] + "/looks/", "cc", "/shows/bluebolt/tools/ocio/looks/None.cc")
  for item in track.items():
    addOcioFileTransformEffectsToTrackItem(item, track, "OCIOFileTransform", os.environ['OCIO_PATH'] + "/luts/", "cube", os.environ['OCIO_PATH'] + "/luts/client.cube", "client_cube")
  for item in track.items():
    addOcioColourSpaceToTrackItem(item, track, targetSpace=None, sourceSpace=None)
 # deleting the last subtrack attached to the dummy track item flattens the timeline
  a = track.subTrackItems()
  track.removeSubTrackItem(a[-1][-1])


def setupColourForTrack2(trackName):
  track = getTrackByName(trackName)
  for item in track.items():
    tli = item.timelineIn()
    ts = item.source()
    createTrackItem(track, item.source().name(), ts, None, tli)
  # create a duplicate dummy track item for last one so we can remove it.
  createTrackItem(track, item.source().name(), ts)
  for item in track.items():
    setTrackItemSourceColourbyName(item)
    addOcioFileTransformEffectsToTrackItem(item, track, "OCIOFileTransform", os.environ['OCIO_PATH'] + "/looks/", "cc", "/shows/bluebolt/tools/ocio/looks/None.cc")
    addOcioFileTransformEffectsToTrackItem(item, track, "OCIOFileTransform", os.environ['OCIO_PATH'] + "/luts/", "cube", os.environ['OCIO_PATH'] + "/luts/client.cube", "client_cube")
    addOcioColourSpaceToTrackItem(item, track, targetSpace=None, sourceSpace=None)
 # deleting the last subtrack attached to the dummy track item flattens the timeline
  a = track.subTrackItems()
  track.removeSubTrackItem(a[-1][-1])


def toggleHardMask(sequence=None):
  # find the path to the resources that ship with Hiero
  if sequence is None:
    sequence = hiero.ui.activeSequence()
  resourcesPath = findResourcePath()

  containsInfoStrip = False
  for track in sequence.videoTracks():
    if track.name() == "Info Strip":
      containsInfoStrip = True
    if track.name() == "Hard Mask":
      sequence.removeTrack(track)
      return

  track = VideoTrack("Hard Mask")

  if containsInfoStrip:
    addInfoStrip()
    sequence.addTrack(track)
    addInfoStrip()
  else:
    sequence.addTrack(track)

  cropEffect = track.createEffect("Crop")

  cropExpression = '''
[python -exec {
from hiero.ui import *
from hiero.core import *
import os
import math
sequence = hiero.ui.activeSequence()
rootHeight=sequence.format().height()
rootWidth=sequence.format().width()



cropVal=os.environ.get("HARD_MASK_RATIO")

if cropVal=="square":
  y=0
  x=(rootWidth-rootHeight)/2
  r=rootHeight+(rootWidth-rootHeight)/2
  t=rootHeight
else:
  if ":" in cropVal:
    l=float(cropVal.split(":")[0])
    r=float(cropVal.split(":")[1])
    ratio=l/r
  else:
    ratio=rootWidth/rootHeight
  h=(rootWidth/ratio)

  x=0
  y=math.floor((rootHeight-h)/2)
  r=rootWidth
  t=math.ceil(h+(rootHeight-h)/2)


} ]
'''

  getXExpression = "[python x]"
  getYExpression = "[python y]"
  getRExpression = "[python r]"
  getTExpression = "[python t]"
  cropEffect.node().knob("box").setExpression(cropExpression + getXExpression, 0)
  cropEffect.node().knob("box").setExpression(cropExpression + getYExpression, 1)
  cropEffect.node().knob("box").setExpression(cropExpression + getRExpression, 2)
  cropEffect.node().knob("box").setExpression(cropExpression + getTExpression, 3)


# Set a different working
def addOCIOCDLTransform(trackItem, track, sourceFilePath, extension, fallbackFile=None, ws_env={}, fallbackFileLabel=None, workingSpace=None):

  effect1 = track.createEffect(effectType="OCIOCDLTransform", trackItem=trackItem, subTrackIndex=0)
  # workingSpace = getColourSpaceNameFromTrackItem(trackItem)

  di_look = ws_env.get("DI_LOOK")
  ws_path = trackItem.source().mediaSource().firstpath()
  ws_path = ws_path.replace("/mnt/SSD/_", "/")
  ws_path = ws_path.replace("/mnt/SSD/", "/")
  ws_path = ws_path.replace("/mnt/ssd/_", "/")
  ws_path = ws_path.replace("/mnt/ssd/", "/")
  ws_env = getws.get_workspace_env(ws_path)
  ws = bbw.Workspace(trackItem.source().mediaSource().firstpath())

  if sourceFilePath:

    effect1.node()['read_from_file'].setValue(True)

    sourceFile = sourceFilePath + di_look + "." + extension

    if os.path.exists(sourceFile):

      name = extension + " color transform for " + di_look

      effect1.setName(name)
      effect1.node()['file'].setValue(sourceFile)
    else:
      name = "No shot color data available"
      effect1.setName(name)
      if fallbackFileLabel:
        effect1.setName(fallbackFileLabel)
      effect1.node()['file'].setValue(fallbackFile)

    if os.environ.get("LUT_COLORSPACE") and os.environ.get("LUT_COLORSPACE").lower() not in ["none", "false", "", "default"]:
      source_cs = os.environ.get("LUT_COLORSPACE")
    else:
      source_cs = getColourSpaceNameFromTrackItem(trackItem)

    effect1.node()['working_space'].setValue(source_cs)


def addOOCIOColorSpace(trackItem, track, ws_env={}):
  effect1 = track.createEffect(effectType="OCIOColorSpace", trackItem=trackItem, subTrackIndex=1)

  bblut = ws_env.get("BBLUT")

  effect1.node()['in_colorspace'].setValue("aces")
  effect1.node()['out_colorspace'].setValue("project/lut")
  effect1.node()['key1'].setValue("BBLUT")
  effect1.node()['value1'].setValue(bblut)

  name = "aces_to_project_lut"
  effect1.setName(name)


def addColor(clip, addLut=False):
  ws_path = clip.source().mediaSource().firstpath()
  ws_path = ws_path.replace("/mnt/SSD/_", "/")
  ws_path = ws_path.replace("/mnt/SSD/", "/")
  ws_path = ws_path.replace("/mnt/ssd/_", "/")
  ws_path = ws_path.replace("/mnt/ssd/", "/")
  ws_env = getws.get_workspace_env(ws_path)
  ocio_path = ws_env.get("OCIO_PATH")
  look_format = ws_env.get("LOOK_FORMAT")
  setTrackItemSourceColourbyName(clip)
  addOCIOCDLTransform(clip, clip.parent(), ocio_path + "/looks/", look_format, "/shows/bluebolt/tools/ocio/looks/None.cc", ws_env=ws_env)
  if addLut:
    addOOCIOColorSpace(clip, clip.parent(), ws_env=ws_env)


def removeColor(clip):
  pass


def find_viewer(sequence):
  """Finds a viewer for the passed sequence.
  """
  for widget in QtWidgets.QApplication.allWidgets():
    try:
      if widget.windowTitle() == sequence.name() and "viewer" in widget.objectName():
        widget.setFocus()
      if hiero.ui.activeView().player().sequence() == sequence:
        return hiero.ui.activeView()
      else:
        continue
    except:
      pass
  return None


def find_timeline_editor(item):
  """Finds a timeline editor for the given item.
  """
  # Find the sequence.
  if isinstance(item, hiero.core.TrackItem):
    sequence = item.parentSequence()
  elif isinstance(item, hiero.core.Sequence):
    sequence = item

  # First get the viewer.  If a viewer isn't found, the current viewer will
  # be used and set to the sequence.
  viewer = find_viewer(sequence)
  if not viewer:
    viewer = hiero.ui.currentViewer()
    p = viewer.player()
    p.setSequence(sequence)

  # Ensure the timeline editor is shown.
  tl = hiero.ui.findMenuAction("Show Timeline Editor")
  tl.trigger()

  # Get a starting ui pane then iterate over all of them until the
  # timeline editor is found for the sequence.
  start_view = hiero.ui.activeView()
  np = hiero.ui.findMenuAction("Next Pane")
  while True:
    active_view = hiero.ui.activeView()
    if isinstance(active_view, hiero.ui.TimelineEditor) and active_view.sequence() == sequence:
      return active_view
    elif active_view == start_view:
      break
    else:
      np.trigger()
  return None


def toggleColorspace():
  clips = []
  coloredClips = 0
  uncoloredClips = 0
  sequence = hiero.ui.activeSequence()
  # if clips are selected
  timeline = find_timeline_editor(sequence)

  if timeline and timeline.selection():
    for select in hiero.ui.activeView().selection():
      if type(select) == TrackItem and select.isMediaPresent():
        clips.append(select)

  # Get on all available clips
  else:
    for track in sequence.videoTracks():
      if track.name().lower() not in ["cut_ref", "cut ref", "cut reference", "cut_reference", "info strip", "hard mask", "info_strip", "hard_mask"]:
        for track_item in track.items():
          if track_item.isMediaPresent():
            clips.append(track_item)

  print clips

  # figue out if its an add or takeaway
  for clip in clips:
    doWeAddColor = True
    mutipleLuts = False
    hasLook = False
    hasLut = False

    for effect in clip.linkedItems():
      if effect.node().Class().startswith("OCIOCDLTransform"):
        hasLook = True
      if effect.node().Class().startswith("OCIOColorSpace"):
        hasLut = True

    if os.environ.get("MULTIPLE_LUTS") and os.environ.get("MULTIPLE_LUTS").lower() == "true":
      mutipleLuts = True

    if mutipleLuts:
      doWeAddColor = not(hasLut and hasLook)
    else:
      doWeAddColor = not hasLook

    if not clip.isEnabled():
      doWeAddColor = False

    if doWeAddColor:
      try:
        addColor(clip, addLut=mutipleLuts)
      except Exception, e:
        traceback.print_exc()

    else:
      removeColor(clip)
    # else:
    #   removeColor(clip)
