from PySide2 import QtGui, QtWidgets

# Custom test action class
class testAction(QtWidgets.QAction):
    def __init__(self):
        QtWidgets.QAction.__init__(self, "newAction", None)
        self.setObjectName('newAction')
        self.triggered.connect(self.doit)

    def doit(self):
        print 'new action using Ctrl+Shift+S'

# Definition to Remove default save shortcut via finding the registered action, and removing the shortcut.
def unregisterDefaultProjectSave():
    registeredActions = hiero.ui.registeredActions()
    for action in registeredActions:
        # If default saveas function is found, remove the shortcut, and disable + hide the action from the menu
        if 'foundry.project.saveas' in action.objectName():
             action.setShortcuts('')
             action.setEnabled(False)
             action.setVisible(False)


# Remove default save shortcut
unregisterDefaultProjectSave()

# Add new action
menu_bar = hiero.ui.menuBar() 
file_action = [action for action in menu_bar.actions() if action.text().lower() == 'file'][0] 

newAction = testAction()
hiero.ui.registerAction(newAction)

# Set shortcut to default save shortcut
newAction.setShortcut("Ctrl+Shift+S")

hiero.ui.mainWindow().addAction(newAction)
