import hiero.core
import nuke
from hiero.exporters.FnShotProcessor import ShotProcessorPreset
import datetime

### Definition to Add Custom Export Token to 'Process as Shots' ONLY ###
def shot_addUserResolveEntries(self, resolver):
    now = datetime.datetime.now()
    
    def AMPM_NEW(task, now):
        resolvedPath = task.resolvedExportPath()
        resolvedFolder = os.path.split(os.path.abspath(resolvedPath))
        AMPM = now.strftime('%p')
        result = AMPM
        if os.path.exists(resolvedFolder[0]):
            #userInput = nuke.getInput('Existing path, add variable?', '')
            userInput = '.EXISTING_FOLDER'
            result = AMPM + userInput
            
        return result
    

    resolver.addResolver("{AMPM-TEST}", "Modified {AMPM} resolver, checks if folder exists, then adds appended numbers", lambda keyword, task: AMPM_NEW(task, now))
        

# Add the Custom Export Token 'Process as Shots' ONLY
ShotProcessorPreset.addUserResolveEntries = shot_addUserResolveEntries

