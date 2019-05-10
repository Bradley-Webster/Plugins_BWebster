from hiero.core import events
import nuke

# Register new callback (Calls whenever the timeline is changed)
events.registerEventType( "kTimelineClipChanged" )

previousClip = None
currentClip = None
def isClipSame():
    # Globally kept variable of last selected clip
    global previousClip
    # try statement catches if user isnt selecting a clip 
    try:
        currentClip = hiero.ui.currentViewer().player().sequence().trackItemAt(hiero.ui.currentViewer().time())
        # Used before selecting first clip
        if previousClip == None:
            previousClip = currentClip.currentVersion()
            return False
        # Version object name comes in as '*name*.v001', this splits out the int version
        ccToString = currentClip.currentVersion().name().split('.')
        pcToString = previousClip.name().split('.')
        ccVersion = ccToString[1][-3], ccToString[1][-2], ccToString[1][-1]
        pcVersion = pcToString[1][-3], pcToString[1][-2], pcToString[1][-1]
        ccVersion = reduce(lambda rst, d: rst * 1 + d, (ccVersion))
        pcVersion = reduce(lambda rst, d: rst * 1 + d, (pcVersion))


        # If both clips are the same version, exit callback
        if currentClip.currentVersion() == previousClip:
            return True
        # If the Current clip version is higher by one, use this command
        elif int(ccVersion) == int(pcVersion)+1:
            nuke.tprint('Current clip has been upversioned once:', ccToString[1])
            previousClip= currentClip.currentVersion()
            return True
        # If the Current Clip version is lower by one, use this command
        elif int(ccVersion) == int(pcVersion)-1:
            nuke.tprint('Current clip has been downversioned once:', ccToString[1])
            previousClip= currentClip.currentVersion()
            return True
        # If the Current Clip is up or downversioned by more than one, print out version, use this command
        elif ccToString[0] == pcToString[0]:
            nuke.tprint('Current clip has been edited, new version:', ccToString[1])
            previousClip= currentClip.currentVersion()
            return True
        else:
            # If the clips are different call the 'newClipSelected' definition
            previousClip= currentClip.currentVersion()
            events.sendEvent( "kTimelineClipChanged", None )
            return False

    except (ValueError, RuntimeError, TypeError, NameError, IndexError):
        return False

nuke.addKnobChanged(isClipSame)

def newClipSelected(event):
    # Your function here if timeline clip changes
    nuke.tprint('New clip Selected')


events.registerInterest("kTimelineClipChanged", newClipSelected)
