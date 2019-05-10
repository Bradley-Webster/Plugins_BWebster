'''
Name: Custom Save As Action Menu
Version: 1.0
Created by: Bradley Webster - Foundry Customer Support Engineer

Description:
    Displays the dynamic naming of the "Save As (...)" Menu action
    within NukeStudio/Hiero.

    Additionally displays how to disable/hide default actions.
'''

from PySide2 import QtGui, QtWidgets
import hiero.core , hiero.ui
import nuke

# Custom test action class
class SaveActionTesting(QtWidgets.QAction):

    def __init__(self):
        QtWidgets.QAction.__init__(self, 'CUSTOM Save As (...)', None)
        self.setObjectName('foundry.project.SaveActionTesting')
        self.triggered.connect(self.doit)

    def doit(self):
        nuke.message('new action using Ctrl+Shift+S')

# Definition to Remove default save shortcut via finding the registered action, and removing the shortcut.
def unregisterDefaultProjectSave():
    registeredActions = hiero.ui.registeredActions()
    for action in registeredActions:
        # If default saveas function is found, remove the shortcut, and disable + hide the action from the menu
        if 'foundry.project.saveas' in action.objectName():
             action.setShortcuts('') 
             # Actions to disable and hide the action from the menu
             if action.isEnabled():
                 action.setDisabled(True)
             if action.isVisible():
                 action.setVisible(False)
                 
# Dynamically change name of action, depending on selected project
def dynamicProjectName(event):
    registeredActions = hiero.ui.registeredActions()
    actionName = 'CUSTOM Save As'
    # Try and Except brackets for use when loading project initally ( Nothing will be selected ) 
    try:
        selection = event.sender.selection()
        for action in registeredActions:
            if 'foundry.project.SaveActionTesting' in action.objectName():
                action.setText(actionName + ' (' + selection[0].project().name() + ')')
    except:
        for action in registeredActions:
            if 'foundry.project.SaveActionTesting' in action.objectName():
                action.setText(actionName + ' (' + hiero.core.projects()[0].name() + ')')

    # Run definition to hide default save action
    unregisterDefaultProjectSave()
             
SaveActionTesting = SaveActionTesting()
hiero.ui.registerAction(SaveActionTesting)

# Set shortcut to default save shortcut
SaveActionTesting.setShortcut("Ctrl+Shift+S")

# Add the new action Before the default Save As Shortcut 
hiero.ui.addMenuAction("foundry.menu.file", SaveActionTesting, before="foundry.project.saveas")

# Register dynamic action name change on ititial load/creation of project
hiero.core.events.registerInterest("kAfterProjectLoad", dynamicProjectName)
hiero.core.events.registerInterest("kAfterNewProjectCreated", dynamicProjectName)
hiero.core.events.registerInterest("kAfterProjectClose", dynamicProjectName) 

# Register dynamic action name change when selection is changed
hiero.core.events.registerInterest("kSelectionChanged/kBin", dynamicProjectName)
