'''
Created by: Bradley Webster - FOUNDRY SUPPORT ENGINEER

Description: On creation of a NEW project, a Sync folder is added.
             Whenever the Project bin selection is altered, Hiero will check if the folder has new files.
             If new files are added, it will add the files to the already created folder.
'''

# Import Hiero statements
from hiero.core import *
from hiero.ui import *

# Set the Following Variable for your SYNC folder location
FOLDERPATH = 'E:\Users\PC_SYD_PC2_E_Drive\Pictures\Test_Footage\SYNC_FolderTest'


def addSYNCFolderOnNewProjectCreation(event):
  ''' Add SYNC folder on Startup'''
  thisProject = projects()[-1]
  clipsBin = thisProject.clipsBin()
  clipsBin.importFolder('E:\Users\PC_SYD_PC2_E_Drive\Pictures\Test_Footage\SYNC_FolderTest')


# OPTION 1

# Add SYNC folder to ALL new projects
# Add event to be called after creation of project
# https://learn.foundry.com/hiero/developers/113/HieroPythonDevGuide/events.html

### UNCOMMENT TO ENABLE ###
events.registerInterest("kAfterNewProjectCreated", addSYNCFolderOnNewProjectCreation) 


def SYNCFolderEvent(event):
  thisProject = projects()[-1]
  clipsBin = thisProject.clipsBin()
  try:
    newBin = clipsBin.importFolder(FOLDERPATH)
    if str(newBin) != "Bin('None')":
      collateDupeBins(clipsBin, newBin)
    print "Sync Complete"
  except:
    print 'Sync Failed.'

def collateDupeBins(clipsBin, newBin):
  ''' Checks if Clips bin has duplicate names, merges bin items and removes new bin '''
  for syncBin in clipsBin.bins():
    # Make sure the syncBin does not equal itslf  (We are looking for older bins)
    if syncBin != newBin:
      # Check if the syncBin has the same name as the newBin
      if syncBin.name() == newBin.name():
        # Collate the newBin items and add them to the original bin
        newBinItems = newBin.items()
        for item in newBinItems:
          syncBin.addItem(item)

        # Remove the newBin after collating the new items
        clipsBin.removeItem(newBin)


# OPTION 2

# Add event to be called after Bin selection is changed
# https://learn.foundry.com/hiero/developers/113/HieroPythonDevGuide/events.html

### UNCOMMENT TO ENABLE ###
events.registerInterest("kSelectionChanged/kBin", SYNCFolderEvent) 