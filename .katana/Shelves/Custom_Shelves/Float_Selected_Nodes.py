"""
NAME: Float Selected
ICON: Icons\Scenegraph\locator32.png
KEYBOARD_SHORTCUT: T
SCOPE:
Created by Bradley Webster - Foundry Customer Support

Float Selected Nodes via Keyboard Shortcut
Quite useful when moving zoomed out nodes

"""

# Get list of selected nodes
nodeList = NodegraphAPI.GetAllSelectedNodes()

# Find Nodegraph tab and float nodes
nodegraphTab = UI4.App.Tabs.FindTopTab('Node Graph')
if nodegraphTab:
    nodegraphTab.floatNodes(nodeList)
