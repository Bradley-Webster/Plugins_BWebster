"""
Python script that creates and registers a custom node type for which parameter
widgets in B{Parameters} tabs are shown with a mini state badge for each
parameter.

Can be placed in the ~/.katana/UIPlugins/ folder to be run during startup in
Katana's UI mode.
"""

import sys
from Katana import FormMaster
from Katana import Nodes3DAPI
from Katana import NodegraphAPI
from Katana import FnGeolibServices
from Katana import FnAttribute
from UI4.FormMaster import EnableableParameterPolicy


def buildParameters(node):
    """
    Creates parameters for the given node.

    @type node: C{Nodes3DAPI.Node3D.Node3D}
    @param node: The node for which to create parameters.
    """
    node.getParameters().createChildNumber('myNumberParameter', 123)
    node.getParameters().createChildString('myStringParameter', 'some text')

def buildOpChain(node, opChainInterface):
    """
    Configures an Op chain for the given node using the given interface object.

    @type node: C{Nodes3DAPI.Node3D.Node3D}
    @type opChainInterface: C{Nodes3DAPI.NodeTypeBuilder.OpChainInterface}
    @param node: The node for which to create an Op chain.
    @param opChainInterface: An object that provides functions for configuring
        an Op chain for the given node.
    """
    # Get the values of certain parameters on the given node
    myNumber = node.getParameter('myNumberParameter').getValue(0)
    myString = node.getParameter('myStringParameter').getValue(0)

    # Configure the Op chain to require no incoming scene graph
    opChainInterface.setMinRequiredInputs(0)

    # Set the path of a location to create by the Op chain
    locationPath = '/root/world/geo/myGroup'

    # Create the arguments for a StaticSceneCreate Op
    staticSceneCreate = FnGeolibServices.OpArgsBuilders.StaticSceneCreate(True)
    staticSceneCreate.createEmptyLocation(locationPath, 'group')
    staticSceneCreate.setAttrAtLocation(locationPath, 'myNumber',
                                        FnAttribute.DoubleAttribute(myNumber))
    staticSceneCreate.setAttrAtLocation(locationPath, 'myString',
                                        FnAttribute.StringAttribute(myString))
    staticSceneCreateOpArgs = staticSceneCreate.build()

    # Add the description of a StaticSceneCreate Op to the Op chain for the
    # given node
    opChainInterface.appendOp('StaticSceneCreate', staticSceneCreateOpArgs)


# Create a node type using NodeTypeBuilder
nodeTypeName = 'NodeWithMiniStateBadges'
print('%s: '
      'Building "%s" node type...'
      % (__file__, nodeTypeName))
nodeTypeBuilder = Nodes3DAPI.NodeTypeBuilder(nodeTypeName)
nodeTypeBuilder.setBuildParametersFnc(buildParameters)
nodeTypeBuilder.setBuildOpChainFnc(buildOpChain)
nodeTypeBuilder.build()

# Register a policy delegate for the node type created above, so that widgets
# for parameters of nodes of that type are shown with mini state badges that
# reflect and control the parameters' useNodeDefault flag
print('%s: '
      'Registering policy delegate for node type "%s"...'
      % (__file__, nodeTypeName))
parameterPolicyDelegate = \
    EnableableParameterPolicy.EnableableScalarPolicyDelegate(exclude=['myStringParameter'])
FormMaster.ParameterPolicy.RegisterPolicyDelegate(nodeTypeName,
                                                  parameterPolicyDelegate)

