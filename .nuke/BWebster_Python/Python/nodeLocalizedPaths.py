'''
Name: nodeLocalizedPaths.py
Created by: Bradley Webster

Description:
    Reviews file dependancies of selected node, checks if they exist within localizedPaths()
    Returns list of node's localized paths
'''

import nuke

def nodeLocalizedPaths(node,first,last):
    localizedPaths = nuke.localization.localizedPaths()
    fileDependencies = node.fileDependencies(first,last)
    localFiles = []

    for dependencies in fileDependencies:
        # LocalizationPath = C:/temp/localize/etc...
        localizationPath = dependencies[1][-1]
        
        # Split down to just the file name e.g "testframe.0001.exr"
        localizationFile = dependencies[1][-1].split('/')[-1]

        for paths in localizedPaths:
            pathFile = paths.split('/')[-1]
            # If the file exists in the path add it ( If not already added to list )
            if  pathFile == localizationFile:
                if paths not in localFiles:
                    localFiles.append(paths)

    # Return a list of the localised paths
    return localFiles

def checkLocalized():
    selectedNode = nuke.selectedNode()

    projectFirst = nuke.root().frameRange().first()
    projectLast = nuke.root().frameRange().last()

    # get the localized Paths from a node and print it in the console
    print nodeLocalizedPaths(selectedNode,projectFirst,projectLast)

