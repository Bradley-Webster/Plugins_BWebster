"""
NAME: TypeMerge
ICON: Icons/SceneGraphView/muteLocal64.png
KEYBOARD_SHORTCUT: Ctrl+M
SCOPE:
Created by: Bradley Webster - Foundry Customer Support

Creates Merge node from selected nodes via keyboard shortcut
Merge Node inputs are set to the type of node (e.g GafferThree = Lighting )

"""

# Global Variable initiation
isType = 0
addedLabel = 0
mergeLabel = ''

# Dictionary collating renderer names
RendererType = {}
RendererType["Prman"] = ['Prman']
RendererType["Delight"] = ['Dl']
RendererType["Arnold"] = ['Arnold']

# Dictionary, collating all names for the Merge nodes
MergeType = {}
MergeType["AOV"] = ['OutputChannelDefine','OutputDefine']
MergeType["Camera"] = ['Camera']
MergeType["Constraint"] = ['Constraint']
MergeType["Filter"]=['Filter']
MergeType["Geometry"] = ['PrimitiveCreate','Alembic','Importomatic','Scenegraph','Pony','AlembicAssetLayout']
MergeType["Group"] = ['GroupMerge', 'GroupStack']
MergeType["Lighting"] = ['GafferThree', 'Light']
MergeType["Image"] = ['Image']
MergeType["Imported"] = ['Alembic','Importomatic','Scenegraph']
MergeType["LiveGroup"] = ['LiveGroup','LiveGroupStack']
MergeType["LookFile"] = ['LookFile']
MergeType["Material"] = ['Material']
MergeType["Merge"] = ['Merge']
MergeType["OCIO"] = ['OCIO']
MergeType["OpScript"] = ['OpScript', 'OpResolve']
MergeType["Render"] = ['Render']
MergeType["Settings"] = ['Settings']
MergeType["Shader"] = ['Shading']
MergeType["Transform"] = ['Transform']


def checkDictionary(node, dictionary):
    """
    Definition used to check dictionaries for matching node types
    """
    # Global variables to check if parts have been met
    global addedLabel
    global isType
    global mergeLabel
    
    # Iterates through given dictionary, if it finds a label, add it to the label name
    for keys,values in dictionary.iteritems():
        for value in dictionary[keys]:
            if value in node.getType():
                # If the dictionary has already found a match, add the new match with an underscore (e.g Alembic_in = Geometry_Imported)
                if addedLabel == 1:
                    mergeLabel+='_' + keys
                else:
                    mergeLabel+=keys
                addedLabel=1
                isType=1

def floatSelectedNodes(selectedNodes):
    '''
    Float all selected nodes in the Node Graph
    '''
    nodegraphTab = UI4.App.Tabs.FindTopTab('Node Graph')
    if nodegraphTab:
        nodegraphTab.floatNodes(selectedNodes)

### EXECUTION of Script Starts HERE ###
        
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

    ### ADD YOUR OWN DICTIONARIES HERE ###
    checkDictionary(n, RendererType)

    checkDictionary(n, MergeType)

    # Once all dictionaries have been checked, add and connect the input port            
    if isType == 0:
        # If the node has no dictionary key, use its type for the port
        merge.addInputPort(n.getType())
    else:
        merge.addInputPort(mergeLabel)
        
    input = merge.getInputPortByIndex(numInputs)
    output.connect(input)

    # Reset Global variables for next node
    isType=0
    addedLabel=0
    mergeLabel = ''


# Set the Merge node as 'selected' and float the node for placement
NodegraphAPI.SetNodeSelected(merge, True)
selectedNode = NodegraphAPI.GetAllSelectedNodes()
floatSelectedNodes(selectedNode)


