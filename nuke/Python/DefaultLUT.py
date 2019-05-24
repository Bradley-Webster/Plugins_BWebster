import nuke
def setNukeColorKnobsDefaults():
    """    Do nuke's color and LUT settings on startup since it mismatches with nukestudio values by default.
    """
    nuke.knobDefault("Root.colorManagement", "OCIO")
    nuke.knobDefault("Root.OCIO_config", "custom")
    nuke.knobDefault("Root.customOCIOConfigPath", "C:/Users/CS_SYD_PC2/.nuke/Workspaces/OCIO/config.ocio")    
    nuke.knobDefault("Root.workingSpaceLUT", "ACES - ACEScg")
    nuke.knobDefault("Root.monitorLut", "ACES - NoGrade")
    nuke.knobDefault("Root.int8Lut", "ACES - ACEScg")
    nuke.knobDefault("Root.int16Lut", "ACES - ACEScg")
    nuke.knobDefault("Root.logLut", "ACES - ACEScg")
    nuke.knobDefault("Root.floatLut", "ACES - ACEScg")

setNukeColorKnobsDefaults()
