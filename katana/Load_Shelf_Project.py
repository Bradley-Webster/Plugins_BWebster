"""
NAME: Load_Shelf_Project
ICON: Icons/LiveGroup/Group256.png

Load specific project file with asset file browser
"""

import os
from Katana import KatanaFile


def LoadProject():
    
    filename = UI4.Util.AssetId.BrowseForAsset('','Select Project File',False,{'fileTypes':'katana *.livegroup'})
    
    if filename is not None:
        KatanaFile.Load(filename)

LoadProject()


