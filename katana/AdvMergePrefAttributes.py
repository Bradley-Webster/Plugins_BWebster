# this function takes the scene graph location where the Alembic asset is to be placed from the Alembic_In node 
# and traverses its child locations to find the actual polymesh location, 
# and then calls checkChildAttrs to find out if they contain the attribute we're interested in.

def findPolyLocationsWithAttributes(client, rootPath, location, port, groupAttr, wildcard, attrDict):
    cookedLocation = client.cookLocation(rootPath + location)
    attrs = cookedLocation.getAttrs()
    type = attrs.getChildByName('type').getValue()
    if type == 'polymesh':
        checkChildAttrs(attrs, port, groupAttr, wildcard, attrDict)       
    else:
        for child in cookedLocation.getPotentialChildren():
            findPolyLocationsWithAttributes(client, (rootPath + location + '/'), child, port, groupAttr, wildcard, attrDict)


# this function uses the group attribute containing the relevant attributes (e.g. 'geometry.arbitrary' so that 
# we don't have to recursively check every single attribute on the location.
# It will check the names of child attributes of this group attribute for any of the strings in the wildcard list
# and create an entry in the {port, attr} dictionary which will be our end result.

def checkChildAttrs(attr, port, groupAttr, wildcard, attrDict):
    groupAttr = attr.getChildByName(groupAttr)
    print groupAttr
    if groupAttr:
        for i in range(groupAttr.getNumberOfChildren()):
            childName = groupAttr.getChildName(i)
            print childName
            matchingName = [name for name in wildcard if name in childName]
            if matchingName:
                attrDict[port.getName()] = childName



# get a runtime instance and a client so we can cook locations to inspect their attributes
runtime = FnGeolib.GetRegisteredRuntimeInstance()
txn = runtime.createTransaction()
client = txn.createClient()

# dictionary of inputs to the merge node mapping to the preferred attributes from that input:
prefAttrsPerInput = {}
# group attribute that contains the specific attributes we're interested in:
groupAttr = 'geometry.arbitrary'
# list of substrings to check the attribute names for:
wildcard = ['st', 'blend_', 'vcol_', 'test_']

node = NodegraphAPI.GetNode('Merge')

for input in node.getInputPorts():
    for port in input.getConnectedPorts():
        connectedNode = port.getNode()
        if connectedNode.getType() == "Alembic_In":
            op = Nodes3DAPI.GetOp(txn, connectedNode)
            txn.setClientOp(client, op)
            runtime.commit(txn)
            nameParam = connectedNode.getParameter('name') 
            findPolyLocationsWithAttributes(client, nameParam.getValue(NodegraphAPI.GetCurrentTime()), '', input, groupAttr, wildcard, prefAttrsPerInput)

# TODO: prefAttrsPerInput dictionary now contains entries in the format {'i1': 'vcol_something'} -
# add corresponding entries to the Merge node's preferredInputAttributes parameter (remember to use full attribute name,
# for example along the lines of name = groupAttr + prefAttrsPerInput['i1']
