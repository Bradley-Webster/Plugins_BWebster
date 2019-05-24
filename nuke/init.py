# Add path to plugins
nuke.pluginAddPath('C:\Users\CS_SYD_PC2\.nuke')
nuke.pluginAddPath('Nukepedia_Plugins/pixelfudger')
nuke.pluginAddPath('plugins')
nuke.pluginAddPath('Python')
nuke.pluginAddPath('Python/Startup')
nuke.pluginAddPath('Python/Startup/Nuke')
nuke.pluginAddPath('Nukepedia_Plugins/timtools')
nuke.pluginAddPath('Nukepedia_Plugins/timtools/gizmos')
nuke.pluginAddPath('Nukepedia_Plugins/timtools/python')
nuke.pluginAddPath('Nukepedia_Plugins/timtools/python/revealExplorer')
nuke.pluginAddPath('Nukepedia_Plugins/timtools/python/newautoBackdrop')
nuke.pluginAddPath('Nukepedia_Plugins/timtools/icons')
nuke.pluginAddPath('BWebster_Python')
nuke.pluginAddPath('BWebster_Python/gizmos')
nuke.pluginAddPath('BWebster_Python/icons')
nuke.pluginAddPath('BWebster_Python/Python')
nuke.pluginAddPath('C:\Users\CS_SYD_PC2\.nuke\spin_nuke_gizmos\gizmos')


nuke.pluginAddPath('engine')

# Add path to favourite directories
nuke.addFavoriteDir('My Pictures' , 'C:\Users\CS_SYD_PC2\Pictures')
nuke.addFavoriteDir('My Videos' , 'C:\Users\CS_SYD_PC2\Videos')
nuke.addFavoriteDir('My Downloads' , 'C:\Users\CS_SYD_PC2\Downloads')
nuke.addFavoriteDir('Desktop' , 'C:\Users\CS_SYD_PC2\Desktop')
nuke.addFavoriteDir('.nuke' , 'C:\Users\CS_SYD_PC2\.nuke')

# knob defaults
nuke.knobDefault('Roto.maskChannelMask','False')
nuke.knobDefault('Roto.maskChannelInput','False')
nuke.knobDefault('Roto.outputMask','False')
nuke.knobDefault('Roto.process_mask','False')
nuke.knobDefault("preferences.ExpressionEvaluationMode", "Always")

#nuke.knobDefault('Read.colorspace','linear')

# TP 353305 workaround - set default font to helvetica by default
nuke.knobDefault( 'preferences.LabelFont', 'helvetica' )

# This will set all nodes with 'note_font' knob default to helvetica
nuke.knobDefault( 'note_font', 'helvetica' )

# Set Project defaults to OCIO colorspace
#nuke.knobDefault('Root.colorManagement', 'OCIO')
#nuke.knobDefault('Root.OCIO_config', 'aces_1.0.3')

prefsNode = nuke.toNode('preferences')
nuke.knobDefault('Preferences.ShowMenusUnderCursor', 'False')
prefsNode.knob('ShowMenusUnderCursor').setDefaultValue([False])
                 
#nuke.ViewerProcess.register("myLUT", nuke.Node, ("myLUT", ""))

nuke.knobDefault('Root.free_type_font_path', 'your/font/path') 

'''
import logging

isGui = nuke.env.get("gui")

logging.basicConfig(filename='C:\Users\CS_SYD_PC2\Documents\Nuke_Projects\LogTest\example.log',level=logging.INFO)
logging.info("Logging from within init.py")
logging.info("GUI: %s\n", isGui)

if isGui == True :
    logging.info("------Running Script in GUI------\n\n")
'''

#nuke.knobDefault('Root.customOCIOConfigPath', os.environ['TESTOCIO'] + '/config.ocio')
#nuke.knobDefault('Root.OCIO_config', 'custom')
#nuke.knobDefault('Root.colorManagement', 'OCIO')


