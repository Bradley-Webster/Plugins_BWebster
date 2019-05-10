"""
Example showing how to override the ScriptWriter class for a Studio/Hiero export
"""

import hiero.core

OriginalScriptWriter = hiero.core.nuke.ScriptWriter

class CustomScriptWriter(OriginalScriptWriter):

  def __init__(self):
    OriginalScriptWriter.__init__(self)

  def addNode(self, node):
    # List of nodes that should actually be added to the script
    nodesToAdd = []

    # node might actually be a list of nodes.  If it is, call onNodeAdded for each one
    if isinstance(node, hiero.core.nuke.Node):
      nodesToAdd.append( self.onNodeAdded(node) )
    else:
      try:
        for n in node:
          nodesToAdd.append( self.onNodeAdded(n) )
      except:
        pass

    # Call base class to add the node(s)
    OriginalScriptWriter.addNode(self, nodesToAdd)

  def onNodeAdded(self, node):
    """ Callback when a node is added. Return the node that should actually be added. """
    if node.type() == "Read": # Change for the type of node you want to edit
      # Make adjustments to all nodes of that type
      node.setKnob("on_error", "black") # This sets each Read nodes missing frames to black
      node.setKnob("auto_alpha", True) # This sets each Read nodes missing frames to black

    return node


hiero.core.nuke.ScriptWriter = CustomScriptWriter
