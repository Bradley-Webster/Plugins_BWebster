import nuke
import os

def nothingSelected():
    inputNodeType = nuke.getInput('Node Type', 'Type Node Type')
    inputNodeType = nuke.allNodes(inputNodeType)
    runScript(inputNodeType)
    
def isSelected():
    if nuke.selectedNodes():
       selectedNodeClass = nuke.selectedNodes()[0].Class()
       selectedNodeClass = nuke.allNodes(selectedNodeClass)
       runScript(selectedNodeClass)
    else:
        nothingSelected()
       
def runScript(nodeClass):
    classExist = 0
    firstNodeState = True
    for n in nodeClass:
        classExist = 1
        if n == nodeClass[0]:
            if n.knob('disable').value() == 0:
               firstNodeState = True
            else:
               firstNodeState = False
        if firstNodeState == True:
           n.knob('disable').setValue(1)
        else:
            n.knob('disable').setValue(0)
    if classExist == 0: 
        nuke.message('That node class does not exist in this script! Please note: nodes are case-sensitive')
