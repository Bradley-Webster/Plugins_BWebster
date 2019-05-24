"""
Output:
NAME: GetWidgetHintsExample
ICON: Icons/comment24.png
SCOPE:
Created by Bradley Webster - Foundry Customer Support

This Shelf tool displays how to get all Widget Hints of a parameter

Some parameters may have no Hint strings, so calling getWidgetHints may display more information

"""


import NodegraphAPI
import UI4.FormMaster

alembicInNode = NodegraphAPI.CreateNode('Alembic_In', NodegraphAPI.GetRootNode())
nameParameter = alembicInNode.getParameter('name')
nameParameterPolicy = UI4.FormMaster.CreateParameterPolicy(None, nameParameter)

print('nameParameter.getHintString() = "%s"' % nameParameter.getHintString())
print('nameParameterPolicy.getWidgetHints() = "%s"' % nameParameterPolicy.getWidgetHints())
