"""
NAME: NameMerge
ICON: Icons/SceneGraphView/muteLocal64.png
KEYBOARD_SHORTCUT: Shift+M
SCOPE:
Created by: Bradley Webster - Foundry Customer Support

Creates Merge node from selected nodes via keyboard shortcut
Merge Node inputs are set to the selected node's name

"""

def floatSelectedNodes(selectedNodes):
    '''
    Float all selected nodes in the Node Graph
    '''
    nodegraphTab = UI4.App.Tabs.FindTopTab('Node Graph')
    if nodegraphTab:
        nodegraphTab.floatNodes(selectedNodes)

# Gets all nodes and their parents
# Create the Merge Node
(nodes, parent) = NodegraphAPI.GetAllSelectedNodesAndParent()
merge = NodegraphAPI.CreateNode("Merge", parent)

# Sort the selected nodes by their position in the Node Graph
nodes.sort(key=NodegraphAPI.GetNodePosition)

# For each node selected, add it to the Merge node
for n in nodes:
    NodegraphAPI.SetNodeSelected(n, False)
    output = n.getOutputPortByIndex(0)
    if not output:
        continue
    numInputs = merge.getNumInputPorts()
    # add and connect the input port with the node's name 
    merge.addInputPort(n.getName())
    input = merge.getInputPortByIndex(numInputs)
    output.connect(input)

NodegraphAPI.SetNodeSelected(merge, True)
selectedNode = NodegraphAPI.GetAllSelectedNodes()
floatSelectedNodes(selectedNode)
