import hiero.core
from hiero.exporters.FnShotProcessor import ShotProcessorPreset

"""
Script created as part of ticket 34044
Used to create Custom Export Tokens within Hiero's export settings
"""

### Definition to Add Custom Export Token to 'Process as Shots' ONLY ###
def shot_addUserResolveEntries(self, resolver):
  resolver.addResolver("{SGversionSHOT}", "Custom version prefix", lambda keyword, task: task.versionString().replace('v', ''))


### Definition to Add Custom Export Token globally ###
def global_addUserResolveEntries(self, resolver):
    resolver.addResolver("{SGversionGLOBAL}", "Custom version prefix", lambda keyword, task: task.versionString().replace('v', ''))



# Add the Custom Export Token to ANY export
hiero.core.TaskPresetBase.addUserResolveEntries = global_addUserResolveEntries


# Add the Custom Export Token 'Process as Shots' ONLY
ShotProcessorPreset.addUserResolveEntries = shot_addUserResolveEntries
