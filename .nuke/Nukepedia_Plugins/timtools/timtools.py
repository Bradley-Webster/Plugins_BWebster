import nuke
import revealExplorer
import newautoBackdrop

myToolbar = nuke.toolbar( 'Nodes' )
myToolbar.addMenu("TimTools", icon="timtools.png")

###HANDY TOOLS### - Tools sourced from Nukepedia
#
###autoBackdrop - Creates a backdrop node with a label attribute, shortcut 'ctrl+b'
myToolbar = nuke.toolbar( 'Nodes' )
myToolbar.addCommand( 'Other/Backdrop',lambda: newautoBackdrop.newautoBackdrop(),'ctrl+b')
#
##HandyGrain - Advanced graining tool using lumininace key to only effect darker areas
myToolbar.addCommand( "TimTools/HandyGrain", "nuke.createNode('HandyGrain')", icon="Grain.png")
#
##Breakdowner - A shot breakdown tool good for showreel breakdowns
myToolbar.addCommand( "TimTools/Breakdowner", "nuke.createNode('Breakdowner')", icon=".png")
#
##revealExplorer - Reveals any file in Explorer
myToolbar=nuke.toolbar('Nodes',)
myToolbar.addCommand('Other/RevealInExplorer',lambda: revealExplorer.revealExplorer(), 'ctrl+e')
#
##ColourSmear - Fixes colour edging issues
myToolbar.addCommand( "TimTools/ColourSmear", "nuke.createNode('ColourSmear')", icon=".png")
#
##CurveGenerator - A tool to create curves to use as sources for expressions
myToolbar.addCommand( "TimTools/CurveGenerator", "nuke.createNode('CurveGenerator')", icon="Clamp.png")
#
##PMatte - Creates a matte using the point pass generated from a 3d application
myToolbar.addCommand( "TimTools/PMatte", "nuke.createNode('PMatte')", icon=".png")
#
##flockBirds - A quick way to add particle driven roto birds to the shot
myToolbar.addCommand( "TimTools/FlockOfBirds", "nuke.createNode('FlockBirds')", icon=".png")

###TIMTOOLS### - Tools adapted and/or created by Tim
#
##ChromaticAberrationPlus - A Chromatic Aberration tool that allows control for red, green and blue aberration
myToolbar.addCommand( "TimTools/ttChromaticAberrationPlus", "nuke.createNode('ttChromaticAberrationPlus')", icon=".png")
#
##PMattePlus - Based on PMatte, this tool lets you us an RGB point pass and provides basic controls in one node
myToolbar.addCommand( "TimTools/ttPMattePlus", "nuke.createNode('ttPMattePlus')", icon=".png")
#
##ttSuperGrade - A grade node that has moe functionality than a standard node
myToolbar.addCommand( "TimTools/ttSuperGrade", "nuke.createNode('ttSuperGrade')", icon=".png")
#
##SalimSplitter - Colour-based matte pulling tool (Good for multi-coloured ID mattes)
myToolbar.addCommand( "TimTools/ttSalimSplitter", "nuke.createNode('ttSalimSplitter')", icon=".png")
#