'''
Name: Export Offline Files To Text File
Version: 1.0
Created by: Bradley Webster - Foundry Customer Support Engineer

Description:
    Adds an action which reviews the Project's MediaSource files for offline files.

    Once offline files are found, they are exported into a Text file, in the saved project location.
'''


from PySide2 import QtGui, QtWidgets
import hiero.core , hiero.ui
import nuke
    
class ExportOfflineFileList(QtWidgets.QAction):
    '''
        This class creates a QAction, which is used to collate all Offline Files within a NukeStudio sctipt
        and add them to a list.

        Once in a list, the list is exported to a text file named "[Project Path]_offlineFileList.txt"

        If there is no list, it will not export and let the user know.
    '''
    
    def __init__(self):
        QtWidgets.QAction.__init__(self, 'Collate and Export Offline File list', None)
        self.setObjectName('foundry.project.collateOfflineFiles')
        self.triggered.connect(self.doit)

    def doit(self):
        print '\nChecking Project for Offline Files'
        offlineFiles = self.getAllOfflineTracks()

        if offlineFiles != []:
            print 'Offline Files Found! Saving offline list to .txt file'
            projects= hiero.core.projects()

            exportPath = projects[-1].path() + '_offlineFileList.txt'
            
            outfile = open(exportPath, "w")

            for item in offlineFiles:
              outfile.write('%s\n' % item)

            outfile.close()
            print '\nExport Complete'
            print 'Saved File destination: ' + exportPath
            nuke.message('Export Complete!\n\nSaved File destination:\n' + exportPath)
        else:
            print 'No Offline Files detected, exiting... '
            nuke.message('No Offline Files detected, exiting... ')

    def getAllOfflineTracks(self):
        offlineFiles = []
        projects= hiero.core.projects()

        sequences = projects[-1].sequences()
        for seq in sequences:
                videoTracks = seq.videoTracks()
                for videoTrack in videoTracks:
                    videoTrackItems = videoTrack.items()
                    for trackItem in videoTrackItems:
                        trackMediaSource = trackItem.source().mediaSource()
                        if trackMediaSource.isOffline():
                            offlineFiles.append(trackMediaSource.filename())

        return offlineFiles

ExportOfflineFileList = ExportOfflineFileList()
hiero.ui.registerAction(ExportOfflineFileList)

# Set shortcut to default save shortcut
ExportOfflineFileList.setShortcut("Ctrl+Shift+O")

# Add the new action Before the default Save As Shortcut 
hiero.ui.addMenuAction("foundry.menu.project", ExportOfflineFileList, before="foundry.project.openInOSShell")
