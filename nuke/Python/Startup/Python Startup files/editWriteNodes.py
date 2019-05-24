'''
Created by: Bradley Webster - Foundry - Customer Support Engineer
Script was created in relation to ZenDesk ticket #26153 Editing write node format of multiple comps
Version: 1.0
'''

import nuke
import nukescripts
from nukescripts import *
import hiero
import os

# GUI selection choices added
compositions = ''
imageType = ''
versionUp = False
project = ''
sequences = ''
sequenceName = ''
sequenceTracks = ''

def editCompsUI():
    project = hiero.ui.activeSequence().project()
    sequences = project.sequences()
    sequenceName = hiero.ui.activeSequence()
    sequenceTracks = sequenceName.items()

    '''
    GUI Interface
    :return:
    '''

    p = nuke.Panel('Edit Comp File Formats')
    dir(p)
    p.addEnumerationPulldown('Selection Type:', 'Selected-Comps All-Comps')
    p.addEnumerationPulldown('Image Format:', 'jpg png tif exr dpx')
    p.addEnumerationPulldown('Version Up compositions?', 'yes no')
    p.addButton('Cancel')
    test= p.addButton('Continue')
    ret = p.show()

    # If the user decides to continue:
    if ret == 1:
        compositions = p.value('Selection Type:')
        imageType = '.' + p.value('Image Format:')
        if p.value('Version Up compositions?') == 'yes':
            versionUp = True
        else:
            versionUp = False

        # If the user selected 'Current_Selection' only edit the current selections, if not, edit all shots
        if compositions == 'Selected-Comps':
            editSELECTEDComp(imageType, versionUp)
        else:
            editALLComps(imageType, versionUp)

def editALLComps(imageType, versionUp):
    '''
    Definition which loops through
    every shot in the current sequence
    to find their filepath.

    :param imageType:
    :param versionUp:
    :return:
    '''
    # Loop through the video tracks and find their filepath
    sequenceName = hiero.ui.activeSequence()
    for item in hiero.ui.activeSequence().project().videoTrackItems():
        fullPath = item.source().mediaSource().firstpath()
        filename, file_extension = os.path.splitext(fullPath)
        # If the file is a Nuke Script, open the file & edit the write nodes
        if file_extension == '.nk':
            editComposition(imageType, fullPath, versionUp)

    message = 'ALL Nuke scripts in Sequence updated.'
    nuke.message(message)

def editSELECTEDComp(imageType, versionUp):
    '''
    Definition which only processes
    the currently selected tracks
    to find their filepath.

    :param imageType:
    :param versionUp:
    :return:
    '''

    selectedTracks= hiero.ui.activeView()
    print selectedTracks
    trackItems = selectedTracks.selection()
    for items in trackItems:
            # Filepaths for shots are found inside the Media Source Metadata values
            TrackItemClip= items.source()
            clipMediaSource = TrackItemClip.mediaSource()
            mediaSourceMetaData = clipMediaSource.metadata()

            # For video tracks it will find their image file (e.g. test.png 1001-1100)
            # For Nuke tracks it will find their Nuke file (e.g. NukeScript.nk)
            fullPath = mediaSourceMetaData.value("foundry.source.path")

            filename, file_extension = os.path.splitext(fullPath)

            # If the file is a Nuke Script, open the file & edit the write nodes
            if file_extension == '.nk' :
                print 'done'
                #editComposition(imageType, fullPath, versionUp)

    message = 'SELECTED Nuke scripts in Sequence updated.'
    nuke.message(message)

def editComposition(imageType, fullPath, versionUp):
    '''
    Definition opens the Nuke script at the selected path
    - Selects ALL write nodes
    - Edits write nodes with new imageType
    - Saves & Closes Nuke Script

    :param file_extension:
    :param fullPath:
    :param versionUp:
    :return:
    '''

    # Open Nuke script at given path
    nuke.scriptOpen(fullPath)
    newExtension = imageType
    # Default value 6 eqauls 'jpg' in the write node dropdown table
    extensionNumber = 6
    n = nuke.allNodes()

    # The write Node's filetype is an array, these numbers relate to their filetype's position
    if newExtension == '.png':
        extensionNumber = 10
    elif newExtension == '.tif':
        extensionNumber = 13
    elif newExtension == '.exr':
        extensionNumber = 3
    elif newExtension == '.dpx':
        extensionNumber = 2
    else:
        # Else set fileType as 'jpg'
        extensionNumber = 6

    # loop through all nodes, find Write Nodes
    for i in n:
        if i.Class() == "Write":
            i.knob("selected").setValue(True)
            # Get current filePath
            testReplace=i.knob("file").getValue()
            # Split filePath, replace old extension with new extension
            testReplace = os.path.splitext(testReplace)[0]+ newExtension
            # Replace file with new FileType
            i.knob("file").setValue(testReplace)
            # The write node has an array for file types, it uses a number position instead of a string name.
            i.knob("file_type").setValue(extensionNumber)

    # If the user chose to 'Version Up' their Nuke Comps, the files are automatically versioned.
    if versionUp == True:
        nukescripts.script.script_version_up()
    # If they choose not to, they are saved normally.
    else:
        nuke.scriptSave("")

    nuke.scriptClose()
    maxSequenceVersions()

def maxSequenceVersions():
    '''
    Step through the current NukeStudio sequence and grab each item's Max Version.
    :return:
    '''
    for item in hiero.ui.activeSequence().project().videoTrackItems():
        item.maxVersion()


menubar=nuke.menu("Nuke")

m=menubar.addMenu("&Custom")

m.addCommand("&Edit Comp File Formats", lambda: editWriteNodes.editCompsUI(), "Ctrl+Shift+e")




