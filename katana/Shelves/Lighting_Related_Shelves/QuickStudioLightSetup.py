"""
NAME: QuickStudioLightSetup
ICON: Icons/Scenegraph/light128.png
KEYBOARD_SHORTCUT: 
SCOPE:
Quick 3 point light setup for your scene

"""

# The following symbols are added when run as shelf buttons:
# exit():      Allows 'error-free' early exit from the script.
# dropEvent:   If your script registers DROP_TYPES, this is a QDropEvent
#              upon a valid drop. Otherwise, it is None.
#              Example:  Registering for "nodegraph/nodes" DROP_TYPES
#                        allows the user to get dropped nodes using
#       nodes = [NodegraphAPI.GetNode(x) for x in
#               str(dropEvent.encodedData( 'nodegraph/nodes' )).split(',')]
# console_print(message, raisePanel = False):
#              If the Python Console exists, print the message to it.
#              Otherwise, print the message to the shell. If raisePanel
#              is passed as True, the panel will be raised to the front.

from Katana import NodegraphAPI

# Take a list of nodes, and merge their outputs
def MergeNodes(nodes, parent):
    merge = NodegraphAPI.CreateNode('Merge')
    merge.setParent(parent)

    for n in nodes:
        output = n.getOutputPortByIndex(0)
        if not output:
            continue
        numInputs = merge.getNumInputPorts()
        inputPort = merge.addInputPort('i%d' % numInputs)
        output.connect(inputPort)

    return merge

# Create a few lightCreates
allLightNodes = []
for lightName in ['key','fill','rim','bounce']:
    lightNode = NodegraphAPI.CreateNode('LightCreate', NodegraphAPI.GetRootNode())
    lightNode.setName(lightName)

    scenegraphLocation = '/root/world/lgt/%s' % lightName
    lightNode.getParameter('name').setValue(scenegraphLocation, 0)
    allLightNodes.append(lightNode)

# Merge the resulting nodes
mergeNode = MergeNodes(allLightNodes, NodegraphAPI.GetRootNode())

# Set reasonable positions
x,y = 0,0
for n in allLightNodes:
    NodegraphAPI.SetNodePosition(n,(x, y))
    x+=100
NodegraphAPI.SetNodePosition(mergeNode,(x-250,y-200))

