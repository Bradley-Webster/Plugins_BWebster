def disableRead():
    nuke.message('Node disabled, Please use "CUSTOM" node Instead')

    nuke.thisNode().knob('disable').setValue(True)

nuke.addOnUserCreate(disableRead, nodeClass='Read')


nuke.toolbar('Nodes').addCommand('Color/Grade', lambda: nuke.message('Node disabled, Please use "CUSTOM" node Instead'), 'g')

nuke.toolbar('Nodes').addCommand('Image/Read', lambda: nukescripts.create_read(defaulttype='Write'), 'r')

nuke.toolbar('Nodes').addCommand('Filter/Blur', lambda: nuke.createNode('NoOp'), 'b')
