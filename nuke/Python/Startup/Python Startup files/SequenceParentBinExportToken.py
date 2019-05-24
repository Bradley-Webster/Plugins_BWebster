import hiero.core
from hiero.exporters.FnShotProcessor import ShotProcessorPreset

### Definition to Add Custom Export Token to 'Process as Shots' ONLY ###
def shot_addUserResolveEntries(self, resolver):

    # Definition is used to find the sequence's parentBin which is currently being exported
    def sequenceList(task, ParentLevel):
        sequenceList = hiero.core.findItemsInBin(hiero.core.projects()[0].clipsBin(), hiero.core.Sequence, task.sequenceName())
        for sequences in sequenceList:
            if ParentLevel == 0:
                sequenceBin = sequences.binItem().parentBin().name()
            elif ParentLevel == 1:
                sequenceBin = sequences.binItem().parentBin().parentBin().name()
            if sequenceBin == '':
                pass
            else:
                return sequenceBin
        # If no parent bin, return the following:
        noParent = 'No_Parent_Bin'
        return noParent

    resolver.addResolver("{SequenceParentBin}", "Custom version prefix", lambda keyword, task: str(sequenceList(task, 0)))
    resolver.addResolver("{SequenceParentBin1}", "Custom version prefix", lambda keyword, task: str(sequenceList(task, 1)))

# Add the Custom Export Token 'Process as Shots' ONLY
ShotProcessorPreset.addUserResolveEntries = shot_addUserResolveEntries
