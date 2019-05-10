"""
NAME: PrintHints
ICON: Icons/comment24.png
DROP_TYPES:
SCOPE:

This is for testing
"""

import os
from Katana import KatanaFile


shader_network_group = NodegraphAPI.GetNode('Shading_Network')
shader_network_nodes = shader_network_group.getChildren()


for shader_network_node in shader_network_nodes:
    parameters = shader_network_node.getParameters().getChild('parameters')

    if parameters:
        parameters_obj = parameters.getChildren()
    
        for parameter_obj in parameters_obj:
            pp = UI4.FormMaster.ParameterPolicy.CreateParameterPolicy(None, parameter_obj)

            if pp:
                print pp.getName()
                print pp.getWidgetHints()
                #hints = pp.getWidgetHints()

                #print hints
                print '---------------------------------------'


