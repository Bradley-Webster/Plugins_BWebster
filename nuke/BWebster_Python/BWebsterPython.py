'''
Name: BWebsterPython.py
Created by: Bradley Webster

Description:
    Adds all plugins/preferences settings to Nuke & NukeX
    Created for personal use
'''

import nuke
import nukescripts
import os
import sys

import customCurveExample
import createConstantFromPicker
import nodeLocalizedPaths
import onErrorToggle
import readReplacement
import rotoShapeExample
import flipbookOnSelected

myToolbar = nuke.toolbar( 'Nodes' )
myToolbar.addMenu("BWebster_Plugins", icon="WebsterLogo.png")

## BurnInTCL - Custom Burn In Node for Hiero ( also useable in Nuke)
##            Adds TCL/Python expression functionality
myToolbar.addCommand( "BWebster_Plugins/BurnIn-TCL", "nuke.createNode('BurnInTCL')", icon=".png")

## Write_FileType_Replace - Replaces all Write node image types when used.
##                         Useful for quickly switching all nodes to another format when preview rendering
myToolbar.addCommand( "BWebster_Plugins/Write Replace FileType ", "nuke.createNode('Write_FileType_Replace')", icon=".png")

## backdropRecolour - recolour all or specific backdrops in your Node Graph
myToolbar.addCommand( 'BWebster_Plugins/Backdrop Recolour',"nuke.createNode('backdropRecolour')")

## Spotlight - Creates 2D Spotlight effect
##            Gizmo can be published after setting up spotlight
myToolbar.addCommand( "BWebster_Plugins/Spotlight BlinkScript", "nuke.createNode('Spotlight')", icon=".png")

## customCurveExample - Example script to display Curve Editor sloped input
myToolbar.addCommand( 'BWebster_Plugins/Custom Curve Example',lambda: customCurveExample.create_curve())

## createConstantFromPicker - Creates a Constant with the Color Picker's current colour
myToolbar.addCommand( 'BWebster_Plugins/Create Constant From Picker',lambda: createConstantFromPicker.createConstant())

## nodeLocalizedPaths - Reviews file dependencies of selected node, checks if they exist within localizedPaths
myToolbar.addCommand( 'BWebster_Plugins/Node Localized Paths',lambda: nodeLocalizedPaths.checkLocalized())

## onErrorToggle - Toggles Read nodes with missing frames between black and nearest frame
myToolbar.addCommand( 'BWebster_Plugins/On Error Toggle',lambda: onErrorToggle.toggleError())

## readReplacement - Toggles Read nodes with missing frames between black and nearest frame
myToolbar.addCommand( 'BWebster_Plugins/Read Replacement',lambda: readReplacement.readCallback(), 'r')

## rotoShapeExample - Toggles Read nodes with missing frames between black and nearest frame
myToolbar.addCommand( 'BWebster_Plugins/RotoShape Example',lambda: rotoShapeExample.pythonRotoExample())

## flipbookOnSelected - Run a Flipbook window with User chosen frame on a selected read node
myToolbar.addCommand( 'BWebster_Plugins/Flipbook On Selected',lambda: flipbookOnSelected.runFlipbook())

## disableNodes - disables node classes of selected nodes, if no nodes selected, ask user for input
myToolbar.addCommand( 'BWebster_Plugins/Disable Nodes',lambda: disableNodes.isSelected())

