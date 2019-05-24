#New autobackdrop
import newautoBackdrop
myToolbar = nuke.toolbar( 'Nodes' )
myToolbar.addCommand( 'Other/Backdrop', lambda: newautoBackdrop.newautoBackdrop(), icon='Backdrop.png' )
