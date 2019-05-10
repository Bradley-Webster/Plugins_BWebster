from hiero.core import *
import hiero.core, hiero.ui
from PySide2.QtCore import QTimer 

def removeSequence(clipsBin):
  # REMOVE the TEMP sequence
  clipsBin.removeItem((clipsBin.sequences()[-1]))


def addFormatOnNewProjectCreation(event):
  # Format size initialization
  width = 1000
  height = 1000
  pixel_aspect = 1
  name = 'New_Test_Format'

  # Create TEMP project to add new format to
  myProject = projects()[-1]
  sequence = Sequence("Format_Addition_Sequence")
  clipsBin = myProject.clipsBin()
  clipsBin.addItem(BinItem(sequence))

  # Create new Format
  testFormat = Format(width, height, pixel_aspect, name)
  sequence.setFormat(testFormat)

  # Open the TEMP Sequence in the Viewer
  # The sequence must be displayed atleast ONCE to register the new Custom Format.
  hiero.ui.openInViewer(BinItem(sequence))

  # Use a QTimer call to allow the Viewer display to be called, then immediately delete the TEMP Sequence
  QTimer.singleShot(0, lambda: removeSequence(clipsBin))


# Add event to be called after creation of project
# https://learn.foundry.com/hiero/developers/112/HieroPythonDevGuide/events.html
events.registerInterest("kAfterNewProjectCreated", addFormatOnNewProjectCreation) 