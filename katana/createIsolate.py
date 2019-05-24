treeWidget = UI4.App.Tabs.FindTopTab('Scene Graph').getSceneGraphView().getWidget()


selectedItems = treeWidget.selectedItems()

addList = []

for items in selectedItems:
    addList.append(items.getLocationPath())


# Create a Prune node
myNode = NodegraphAPI.CreateNode('Isolate', NodegraphAPI.GetRootNode())

# Get the CEL parameter (parameter is named 'cel')
celParam = myNode.getParameter('isolateLocations.i0')

# Set the value
#celParam.setValue('[' + ' '.join(addList) + ']',0) 

test =NodegraphAPI.GetNode('Isolate2').getParameter('isolateLocations')


print test.getValue(0)