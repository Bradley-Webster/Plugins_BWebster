import hiero.ui
from hiero.core import events

def eventAfterProj(event):
  print 'eventAfterProj'
  print "Viewer caches flushed and paused"
  hiero.ui.flushAllViewersCache()
  
events.registerInterest("kAfterProjectLoad", eventAfterProj)
