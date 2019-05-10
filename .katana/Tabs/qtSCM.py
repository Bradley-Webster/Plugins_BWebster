
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



class qtsmTab(BaseTab):

    def __init__(self,parent):
        super(qtsmTab, self).__init__(parent)

        options = ["Test Item"]

        vLayout = QtGui.QVBoxLayout(self)
        self.setLayout(vLayout)
        
        self.options = QtGui.QToolButton(self)
        self.options.setText('Preferences')
        self.optionMenu = QtGui.QMenu(self.options)
        
        self.monitorLayerPrefs = []
        for option in (options):
            action = self.optionMenu.addAction(option)
            action.setShortcuts(Qt.QKeySequence(']'))
            action.setCheckable(True)
            action.setChecked(True)
            self.monitorLayerPrefs.append(action)

        optionMapping = QtCore.QSignalMapper(self)
        index = 0
        for action in self.monitorLayerPrefs:
            optionMapping.setMapping(action,index)
            action.triggered.connect(optionMapping.map)
            index = index + 1

        optionMapping.mapped[int].connect(self.testAction)

        self.options.setMenu(self.optionMenu)
        self.options.setPopupMode(QtGui.QToolButton.InstantPopup)

        self.layout().addWidget(self.options)


    def testAction(self):
        print 'test action'


PluginRegistry = [
   ("KatanaPanel", 2.0, "qtSCM", qtsmTab),
   ]
