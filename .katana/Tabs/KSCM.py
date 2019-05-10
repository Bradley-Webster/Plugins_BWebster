
from Katana import (
    QtCore,
    QtGui,
    CatalogManager,
    UI4,
    Utils,
    QT4Widgets,
    ScenegraphManager,
    Nodes3DAPI,
    FnGeolib,
    NodegraphAPI,
    Qt
)

from UI4.Tabs import BaseTab


from UI4.App.KeyboardShortcutManager import (RegisterActions, CreateAction,GetActionID,UpdateAction)



class ksmTab(BaseTab):

    # Class Variables ----------------------------------------------------------

    # The key to use when registering and using keyboard shortcuts
    __CONTEXT_NAME = "KSM Tab"

    def __init__(self,parent):
        super(ksmTab, self).__init__(parent)

        options = ["Test Item"]

        vLayout = QtGui.QVBoxLayout(self)
        self.setLayout(vLayout)
        
        self.options = QtGui.QToolButton(self)
        self.options.setText('Preferences')
        self.optionMenu = QtGui.QMenu(self.options)

        for option in (options):
            action = CreateAction(GetActionID(self.__CONTEXT_NAME,option),self,text=option)
            self.optionMenu.addAction(action)
            action.setCheckable(True)
            action.setChecked(True)

        self.options.setMenu(self.optionMenu)
        self.options.setPopupMode(QtGui.QToolButton.InstantPopup)

        self.layout().addWidget(self.options)


    @classmethod
    def registerKeyboardShortcuts(cls):
        print 'rks',cls
        cls.setShortcutsContextName(cls.__CONTEXT_NAME)
      
        # Dictionary of all actions to register keyboard shortcuts for
        actions = dict()

        actions['Test Item'] = ('Test Item', 'l', cls.testAction)

        # Register actions with shortcut manager.
        RegisterActions(cls.__CONTEXT_NAME, actions)

    def testAction(self):
        print 'test action'


PluginRegistry = [
   ("KatanaPanel", 2.0, "KSCM", ksmTab),
   ]
