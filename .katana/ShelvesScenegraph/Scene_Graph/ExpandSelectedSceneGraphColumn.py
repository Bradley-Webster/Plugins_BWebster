"""
NAME: Expand Selected Scene Graph Column
ICON: Icons/expand16.png
KEYBOARD_SHORTCUT: Q
SCOPE:
Created by Bradley Webster - Foundry Customer Support

This script expands the currently selected Scene Graph Column to view all locations/objects

Add to your .katana/ShelvesScenegraph/ folder location  ( Create it if it does not exist )
"""

def ExpandSelectedColumns():
    treeWidget = UI4.App.Tabs.FindTopTab('Scene Graph').getSceneGraphView().getWidget()
    column = treeWidget.currentColumn()
    treeWidget.resizeColumnToContents(column)
    
ExpandSelectedColumns()
