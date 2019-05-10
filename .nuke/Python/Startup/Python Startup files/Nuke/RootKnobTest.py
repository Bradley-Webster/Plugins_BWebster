import nuke
import os


# Nuke11 +
if nuke.NUKE_VERSION_MAJOR >= 11:
	nuke.toolbar("Edit/pasteall").addCommand('MultiCopy' , 'paste_all()', '+:')

# Nuke10 and below
else:
	nuke.toolbar("Edit/pasteall").addCommand('MultiCopy' , 'paste_all()', '+;')


# Method which returns if Nuke Launched, or 'File > New' is selected

def checkNew():
    nodeClass = nuke.thisNode().Class()
    if nodeClass == 'Root':
        print 'Nuke launched, or new script created'
        return

def checkLoaded():
    nodeClass = nuke.thisNode().Class()
    if nodeClass == 'Root':
        nuke.tprint('TESTING', [{nuke.script_directory()}])
        print 'Existing Script loaded'
        return

# Register the callback
nuke.addOnUserCreate(checkNew)

nuke.addOnScriptLoad(checkLoaded)



nuke.tprint('TESTING', [{nuke.script_directory()}])

nuke.tprint('TESTING', [{os.path.dirname(nuke.script_directory())}])
