'''
Name: menu.py
Used by: Bradley Webster - Foundry Customer Support Engineer

Description:
    Adds all plugins/preferences settings to Nuke & NukeX
'''

# General Nuke imports
import nuke
import nukescripts
import os
import sys

# PySide or PySide2 imports ( depending on version )
if nuke.NUKE_VERSION_MAJOR >= 11:
        from PySide2 import QtCore, QtGui, QtWidgets
	from PySide2.QtCore import QTimer

else:
        from PySide import QtCore


# Import Nukepedia_Plugins Python files
import BWebsterPython
import pixelfudger
import timtools
import newCompWithArguments

def clearBeforeFrame():
    nukescripts.cache_clear('')
    nuke.clearDiskCache()
    nuke.clearRAMCache()
    nuke.tprint( 'Curent memory size BEFORE frame ', nuke.frame(), ' : ', nuke.memory("usage") )


#nuke.addBeforeFrameRender(clearBeforeFrame)

def clearAfterFrame():
    nuke.tprint( 'Curent memory size AFTER_ frame ', nuke.frame(), ' : ', nuke.memory("usage") )


#nuke.addAfterFrameRender(clearAfterFrame)

t = nuke.toolbar( 'Nodes' )
t.addMenu("Image", "ToolbarDraw.png")
t.addCommand('Load Folder', 'nuke.load("recursiveLoad"), recursiveLoad()',  'alt+r', icon='Read.png')

t.addCommand('Other/DisableNodes',lambda: disableNodes.isSelected(), 'shift+d')

def paste_all():
	for node in nuke.selectedNodes():
		node.setSelected(True)
		nuke.nodePaste("%clipboard%")
		node.setSelected(False)


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
        print nuke.root().knob('free_type_font_path').getValue()
        return

def checkLoaded():
    nodeClass = nuke.thisNode().Class()
    if nodeClass == 'Root':
        print 'Existing Script loaded'
        return

# Register the callback
nuke.addOnUserCreate(checkNew)

nuke.addOnScriptLoad(checkLoaded)

# Fork timeline Nuke Script into new nuke comp (NukeStudio)
def OpenTrackInNuke():
        try:
            nuke.fork(hiero.ui.getTimelineEditor(hiero.ui.activeSequence()).selection()[0].source().mediaSource().firstpath()) 
        except IndexError, TypeError:
            nuke.message('No selected track item, please select track item') 


nuke.menu('Nuke').addCommand('Clip/New Nuke Session', 'OpenTrackInNuke()', 'Ctrl+N')

# Callback funtion
def replaceFBX():
    newNode = nuke.thisNode()
    newNodeFilePath = newNode.knob('file').value()
    filename, file_extension = os.path.splitext(newNodeFilePath)
    
    # Review the created node's file extension and check if it is an .fbx file
    
    if file_extension == '.fbx':
        print 'fbx found'
        # Popup panel to alert user of .fbx creation.
        # Panel deletes the ReadGeo Node and creates an Axis2 instead.
        # Feel free to remove the popup panel, if you do not want the warning.
        if nuke.ask('fbx file creation detected, create Axis node instead?'):
            nuke.delete(newNode)
            newAxis = nuke.createNode('Axis2')
            newAxis.knob('read_from_file').setValue(1)
            newAxis.knob('file').setValue(newNodeFilePath)
    else:
        print 'not file extension'

def readCallback():
        # Add the callback, to be called only when ReadGeo2 nodes are created.
        nuke.addOnCreate(replaceFBX, nodeClass='ReadGeo2')

        nukescripts.create_read()
        
        nuke.removeOnCreate(replaceFBX, nodeClass='ReadGeo2')
        
nuke.menu('Nuke').addCommand('Custom/test','readCallback()', 'r')

# Create beforeRender function
def beforeRenderBackup():   
    if nuke.Root().modified() == True:

            if nuke.ask('Save backup script before continuing?'):
                    # Obtain Write node filename, split into directory
                    file = nuke.filename(nuke.thisNode())
                    writePath = os.path.dirname(file) + '/'

                    # Obtain project filename
                    fullProject =  nuke.value("root.name")
                    projectName =  fullProject.split('/')[-1]

                    # Setup backup project name + path
                    projectNameBackup = 'Backup.' + projectName
                    newBackupProject = writePath + projectNameBackup

                    # Setup backup project
                    nuke.scriptSaveAs(writePath)

                    # Set current project back to original project
                    nuke.root().knob('name').setValue(fullProject)

# Add the beforeRender function 
nuke.addBeforeRender(beforeRenderBackup)



toolbar = nuke.menu("Nodes")
m = toolbar.addMenu("Color/artistTools", "ToolbarColor.png")
 
m.addCommand('secondaryColour', 'nuke.createNode("secondaryColour2")', icon='secondaryGrade.png')
m.addCommand('secondaryMattes', 'nuke.createNode("secondaryMattes")', icon='secondaryGrade.png')
m.addCommand("vibrancy", "nuke.createNode(\"vibrancy\")", icon="secondaryGrade.png")

def copySave():
    # Hardcoded folder for file browser save
    sourceSave = 'C:/Users/CS_SYD_PC2/Documents/Nuke_Projects/MovedSave/SaveHere/'
    destinationSave = 'C:/Users/CS_SYD_PC2/Documents/Nuke_Projects/MovedSave/MoveHere/'
     
    # Obtain project filename
    fullProject = nuke.value("root.name")
    projectName = fullProject.split('/')[-1]
    
    # Save project
    if os.path.isfile(fullProject):
        nuke.scriptSave(fullProject)
    else:
        nuke.scriptSaveAs(sourceSave)
     
    # If you wish to use the folder where the script is currently saved, use: 
    # nuke.scriptSaveAs(os.path.dirname(fullProject))
     
    if nuke.ask('Additionally save script to: "' + destinationSave + '" ?'):
        shutil.copy(nuke.value("root.name"), destinationSave)

nuke.menu('Nuke').addCommand('File/copySave', 'copySave()', 'Ctrl+S')

nuke.menu('Nuke').addCommand('Custom/Create Constant From Picker', lambda: createConstantFromPicker.createConstant(), 'Ctrl+Alt+C')

nuke.knobDefault("preferences.ExpressionEvaluationMode", "1")

nuke.menu('Nuke').addCommand('File/New Comp in Safe Mode... ', lambda: newCompWithArguments.newCompWithArguments(), 'Ctrl+Shift+N')

nuke.menu("Nodes").addCommand("Color/OCIO/OCIO LookTransform", 'nuke.createNode("OCIOLookTransform")', icon="OCIO.png")

def reloadLivegroups():
    nodes = nuke.allNodes()
     
    for node in nodes:
        if node.Class() == "LiveGroup":
            node.knob("reload_script").execute()
            print 'LiveGroups reloaded'

#nuke.addOnScriptLoad(reloadLivegroups)

def openRecentProject():
        # Navigate to recent_files located in your .nuke directory
        filename = os.getenv('HOME') + '/.nuke/recent_files'
        f = open(filename, "r")

        # Read the first line, this will be your most recent file.
        mostRecent = f.readline()
        # The line will be appended with a new line, remove it.
        mostRecent = mostRecent.replace('\n','')

        # Close the text file after use
        f.close()

        # Ask the user if they would like to open the recent file.
        if nuke.ask('Recent project detected, would you like to reload it? \n %s' % mostRecent):
                # Close script which is launched with Nuke, then open recent project.
                nuke.scriptExit()
                nuke.scriptOpen(mostRecent)

# Register the callback
# nuke.addOnUserCreate(openRecentProject, nodeClass='Root')

def pasteDropNode(filename, text):
    newNode = nuke.nodePaste(text)
    newNode.setName(filename)

def importGizmo(Type, text):
    # Split text variable to get the filename and extension
    file = os.path.basename(text)
    filename = file.split('.')[0]
    extension = file.split('.')[1]

    # If the file is a .gizmo, 
    if extension == 'gizmo':
        QTimer.singleShot(0, lambda: pasteDropNode(filename, text))
        return True
    return False

nukescripts.addDropDataCallback(importGizmo)


#from PySide2.QtCore import QTimer

def addR3DDefaults(readNode):
   readNode.knob("r3dImagePipeline").setValue('IPP2')
   readNode.knob("r3dExportPipeline").setValue('primary raw development')
   readNode.knob("colorspace").setValue('Input - RED - REDLog3G10 - REDWideGamutRGB')

def R3DDefaultSetup():
    readNode = nuke.thisNode()
    fileKnob = readNode.knob("file").getValue()
 
    if fileKnob.endswith('.R3D'):
        QTimer.singleShot(0, lambda: addR3DDefaults(readNode))

#nuke.addOnCreate(R3DDefaultSetup, nodeClass="Read")

class Foo:
  @staticmethod
  def myTest():
    return "./img.exr"

def DeepReadDisplayWorkaround():
    for n in nuke.allNodes('DeepRead'):
            nuke.show(n)
            n.hideControlPanel()


nuke.addOnScriptLoad(DeepReadDisplayWorkaround)
