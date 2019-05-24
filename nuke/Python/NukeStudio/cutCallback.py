from hiero.core import events

events.registerEventType( "kTimelineClipChanged" )

previousClip = None

def isclipsame():
    global previousClip
    currentClip = hiero.ui.currentViewer().player().sequence().trackItemsAt(hiero.ui.currentViewer().time())
    if currentClip == previousClip:
        previousClip = currentClip
        return True
    else:
        previousClip = currentClip
        events.sendEvent( "kTimelineClipChanged", None )
        return False

nuke.addKnobChanged(isclipsame)

def superPrint(event):
    print "super, the clip has changed"

events.registerInterest("kTimelineClipChanged", superPrint)
