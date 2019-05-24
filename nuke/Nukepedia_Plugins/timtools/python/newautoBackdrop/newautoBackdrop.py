# Copyright (c) 2009 The Foundry Visionmongers Ltd.  All Rights Reserved.

#This is created from autobackdrop.py with a tweaked tile_color to a true random colour.
#When this is called the user will be asked to name the label.
#For more info visit www.harrisonly.co.uk
import nuke, random

def newautoBackdrop():
  '''
  Automatically puts a backdrop behind the selected nodes.
  
  The backdrop will be just big enough to fit all the select nodes in, with room
  at the top for some text in a large font.
  '''
  
  newLabel = nuke.getInput('Backdrop Label:', '')
  
  r = int(nuke.expression('000+255*random()'))
  g = int(nuke.expression('000+255*random()'))
  b = int(nuke.expression('000+255*random()'))
  
  selNodes = nuke.selectedNodes()
  if not selNodes:
    return nuke.nodes.BackdropNode()

  # Calculate bounds for the backdrop node.
  bdX = min([node.xpos() for node in selNodes])
  bdY = min([node.ypos() for node in selNodes])
  bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
  bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY
  
  # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
  left, top, right, bottom = (-10, -80, 10, 10)
  bdX += left
  bdY += top
  bdW += (right - left)
  bdH += (bottom - top)
  
  n = nuke.nodes.BackdropNode(xpos = bdX,
                              bdwidth = bdW,
                              ypos = bdY,
                              bdheight = bdH,
                              tile_color = int('%02x%02x%02x%02x' % (r,g,b,0),16),
                              note_font_size=42,
							  label = '%s' % newLabel)

  # revert to previous selection
  n['selected'].setValue(False)
  for node in selNodes:
    node['selected'].setValue(True)
 
  return n
