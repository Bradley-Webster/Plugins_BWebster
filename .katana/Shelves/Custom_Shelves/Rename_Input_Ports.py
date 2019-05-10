"""
NAME: Rename selected input ports
ICON: Icons/SceneGraphView/soloLocal256.png
DROP_TYPES:
SCOPE:
This is an example script for - "Q100372: Renaming input and output ports with Python"
After the user has selected their desired nodes, using this tool will set their
inputPorts to an increment of 'shot'
"""

import os
from Katana import KatanaFile


selectedNodes = NodegraphAPI.GetAllSelectedNodes()

for node in selectedNodes:
    inputPorts = node.getInputPorts()
    
    for inputs in inputPorts:
        index= inputs.getIndex()
        test = node.getInputPortByIndex(index)
        name = test.getName()
        
        
        node.renameInputPort(name,'Shot1')
