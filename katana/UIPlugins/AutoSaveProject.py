from Katana import QtCore, NodegraphAPI, KatanaFile
import os

# VARIABLES

# Set your save option
saveOption = 1

# Set delay interval for autosaves
# function argument is the interval in milliseconds (10 seconds in this example)
autosaveDelay = 60000

def saveAndSubmit():
	''' Autosaves project with option specified by user '''

	# Get path variables
	projectPath = NodegraphAPI.NodegraphGlobals.GetProjectFile()
	projectFile = os.path.basename(projectPath)
	projectDir = os.path.dirname(projectPath)


	# OPTION 0
	# Q100450: Locating a crash Autosave file - https://support.foundry.com/hc/en-us/articles/360000024960
	# Save a crash file (standard autosave):
	if saveOption == 0:
		KatanaFile.CrashSave(True)

	# Check if file has been saved atleast once.
	if projectPath != '':
		# Check if file has been modified since last save
		if KatanaFile.IsFileDirty():

			# OPTION 1
			# to save file at the current location use:
			if saveOption == 1:	
				KatanaFile.Save(projectPath)

				print "File autosaved to: " + projectPath

			# OPTION 2
			# to save at a specified location use:
			if saveOption == 2:
				# Custom folder directory for Option 2
				customFolderDirectory = 'path/to/desired/location/'

				KatanaFile.Save(customFolderDirectory + projectFile)

				print "File autosaved to: " + customFolderDirectory + projectFile

timer = QtCore.QTimer()
timer.timeout.connect(saveAndSubmit)
timer.start(autosaveDelay) 
