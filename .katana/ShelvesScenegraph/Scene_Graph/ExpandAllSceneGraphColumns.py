"""
NAME: Expand All Scene Graph Columns
ICON: Icons/expandAll16.png
KEYBOARD_SHORTCUT: W
SCOPE:
Created by Bradley Webster - Foundry Customer Support

This script expands the all Scene Graph Columns to view all locations/objects

Add to your .katana/ShelvesScenegraph/ folder location  ( Create it if it does not exist )

"""

def ExpandAllColumns():
    treeWidget = UI4.App.Tabs.FindTopTab('Scene Graph').getSceneGraphView().getWidget()
    for column in range(treeWidget.columnCount()):
        treeWidget.resizeColumnToContents(column)

ExpandAllColumns()
