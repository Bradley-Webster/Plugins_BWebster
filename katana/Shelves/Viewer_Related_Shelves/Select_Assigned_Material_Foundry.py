"""
NAME: Select Scene Graph selection assigned material
ICON: icon.png
KEYBOARD_SHORTCUT: Ctrl+Shift+M
SCOPE:
Selects the Scene Graph selection's assigned material in the Node Graph.

"""
NodegraphAPI.SetAllSelectedNodes('')

# Get currently selected location in the Viewer to use for function
viewer = UI4.App.Tabs.FindTopTab('Viewer (Hydra)')
selected = viewer.getSelectedLocations()
sgt = UI4.App.Tabs.FindTopTab('Scene Graph')
sgv = sgt.getSceneGraphView()
attrs = sgv.getSceneGraphAttributes(selected[0])
mat = attrs.getChildByName('globalMaterialAssign')

# Get the location name for the NodeGraph selection
matName = os.path.split(mat.getValue())[-1]

# Select the location within the Scene Graph
selectedLocs = []
selectedLocs.append(mat.getValue())
sgv.selectLocations(selectedLocs,False)

# Select the location within the Node Graph
materialNodes = NodegraphAPI.GetAllNodesByType('NetworkMaterial')

for materials in materialNodes:
    if materials.getName() == matName:
        NodegraphAPI.SetNodeSelected(materials, 1)