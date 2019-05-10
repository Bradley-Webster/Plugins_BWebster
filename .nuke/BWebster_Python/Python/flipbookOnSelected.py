'''
Name: flipbookOnSelected.py
Version: 1.0
Created by: Bradley Webster

Description: Run a Flipbook on a selected node with the user's frame rate
'''

from nukescripts import flip, flipbooking
import nuke

def runFlipbook():
    try:
        if nuke.selectedNodes()[0].Class() == 'Read':
            filePath = nuke.selectedNodes()[0].knob('file').value()
            fileFirstFrame = nuke.selectedNodes()[0].knob('first').value()
            fileLastFrame = nuke.selectedNodes()[0].knob('last').value()
            fileRange = str(fileFirstFrame) + '-' + str(fileLastFrame)
            ret = nuke.getFramesAndViews('Run Flipbook on Selected Node',fileRange)
            if ret:
                range = ret[0]
                views = ret[1]
                flipbooker = flipbooking.gFlipbookFactory.getApplication('Default')
                flipbooker.run(filePath, nuke.FrameRanges(range), 'main', {})
        else:
            print 'Node Selected not Read node, please select Read node and try again'
    except IndexError:
        print 'No Node Selected, please select Read node and try again'
        
