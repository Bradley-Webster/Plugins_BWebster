# Class to show how to handle drop events in the bin view
from hiero.core.events import *

class TilelineViewDropHandler:
  kTextMimeType = "text/plain"
  
  def __init__(self):
    # hiero doesn't deal with drag and drop for text/plain data, so tell it to allow it
    hiero.ui.registerBinViewCustomMimeDataType(TilelineViewDropHandler.kTextMimeType)
    
    # register interest in the drop event now
    registerInterest((EventType.kDrop, EventType.kTimeline), self.dropHandler)

  def dropHandler(self, event):
    print event
    # more complicated way
    if event.mimeData.hasFormat(TilelineViewDropHandler.kTextMimeType):
      byteArray = event.mimeData.data(TilelineViewDropHandler.kTextMimeType)
      print 'Filename: '
      filename = byteArray.data()
      print filename
        
    # get custom hiero objects if drag from one view to another (only present if the drop was from one hiero view to another)
    if hasattr(event, "items"):
      print "TrackItem"
      trackItem = event.items
      print trackItem

    print filename.split('.')[-1]
    if filename.split('.')[-1] == 'mov':
        print 'file is MOV, replace Audio'

# Instantiate the handler to get it to register itself.
dropHandler = TilelineViewDropHandler()
    