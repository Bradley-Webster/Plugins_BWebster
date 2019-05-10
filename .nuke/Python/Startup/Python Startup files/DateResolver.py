import hiero.core
import nuke
from hiero.exporters.FnShotProcessor import ShotProcessorPreset
import datetime

### Definition to Add Custom Export Token to 'Process as Shots' ONLY ###
def shot_addUserResolveEntries(self, resolver):
    now = datetime.datetime.now()
    
    def AMPM_NEW(task, now):
        #resolvedPath = task.resolvedExportPath()
        resolvedPath = 'C:\Users\CS_SYD_PC2\.nuke\Python\Startup'
        resolve = task.resolvePath(resolvedPath)
        print resolve
        resolvedFolder = os.path.split(os.path.abspath(resolvedPath))
        AMPM = now.strftime('%p')
        result = AMPM
        if os.path.exists(resolvedFolder[0]):
            #userInput = nuke.getInput('Existing path, add variable?', '')
            userInput = '.EXISTING_FOLDER'
            result = AMPM + userInput
            
        return resolve
    

    resolver.addResolver("{AMPM-TEST}", "Modified {AMPM} resolver, checks if folder exists, then adds appended numbers", lambda keyword, task: AMPM_NEW(task, now))
        

# Add the Custom Export Token 'Process as Shots' ONLY
ShotProcessorPreset.addUserResolveEntries = shot_addUserResolveEntries
