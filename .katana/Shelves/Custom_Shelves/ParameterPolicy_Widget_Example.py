"""
NAME: CameraParameterPolicyExample
ICON: Icons/camera16.png
KEYBOARD_SHORTCUT:
SCOPE: This example script will create a small widget made from an CameraCreate Node

"""


import UI4.FormMaster.PythonValuePolicy

# Create a node for which to create parameter widgets
node = NodegraphAPI.CreateNode('CameraCreate', NodegraphAPI.GetRootNode())

# Get a couple of parameters from the node
nameParameter = node.getParameter('name')
projectionParameter = node.getParameter('projection')
fovParameter = node.getParameter('fov')

# Create parameter policies for the parameters
nameParameterPolicy = UI4.FormMaster.CreateParameterPolicy(None, nameParameter)
projectionParameterPolicy = UI4.FormMaster.CreateParameterPolicy(None, projectionParameter)
fovParameterPolicy = UI4.FormMaster.CreateParameterPolicy(None, fovParameter)

# Create a policy to group the above parameter policies, and set a widget hint on it to hide the group's title
myGroupPolicyData = {
    '__childOrder': ['name', 'projection', 'fov'],
}
myGroupPolicy = UI4.FormMaster.PythonValuePolicy.PythonValuePolicy('myGroup', myGroupPolicyData)
myGroupPolicy.addChildPolicy(nameParameterPolicy)
myGroupPolicy.addChildPolicy(projectionParameterPolicy)
myGroupPolicy.addChildPolicy(fovParameterPolicy)
myGroupPolicy.getWidgetHints()['hideTitle'] = True

# Create and show the parameter widgets
groupFormWidget = UI4.FormMaster.KatanaFactory.ParameterWidgetFactory.buildWidget(None, myGroupPolicy)
groupFormWidget.show()
