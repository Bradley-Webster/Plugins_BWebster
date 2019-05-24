import nuke
import nukescripts

# Callback funtion
def replaceFBX():
    newNode = nuke.thisNode()
    newNodeFilePath = newNode.knob('file').value()
    filename, file_extension = os.path.splitext(newNodeFilePath)
    
    # Review the created node's file extension and check if it is an .fbx file
    
    if file_extension == '.fbx' or file_extension == '.FBX':
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
        pass

def readCallback():
        # Add the callback, to be called only when ReadGeo2 nodes are created.
        nuke.addOnCreate(replaceFBX, nodeClass='ReadGeo2')
        nukescripts.create_read()
        nuke.removeOnCreate(replaceFBX, nodeClass='ReadGeo2')
        
