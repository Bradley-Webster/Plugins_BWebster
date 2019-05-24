from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtCore


class MultiComboBoxModel(QStandardItemModel):

    checkStateChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super(MultiComboBoxModel, self).__init__(0, 1, parent)

    def flags(self, index):
        return super(MultiComboBoxModel, self).flags(index) | QtCore.Qt.ItemIsUserCheckable

    def data(self, index, role):
        value = super(MultiComboBoxModel, self).data(index, role)

        if index.isValid() and role == QtCore.Qt.CheckStateRole and value is None:
            value = QtCore.Qt.Unchecked

        return value

    def disconnectNotify(self, *args, **kwargs):
        try:
            super(MultiComboBoxModel, self).disconnectNotify(*args, **kwargs)
        except:
            pass

    def setData(self, index, value, role):
        result = super(MultiComboBoxModel, self).setData(index, value, role)

        if result and role == QtCore.Qt.CheckStateRole:
            try:
                self.dataChanged.emit(index, index)
            except:
                self.dataChanged.emit(index, index, value)
            self.checkStateChanged.emit()
        return result

class CheckableCombo(QComboBox):
    
    selectionConfirmed = QtCore.Signal(int)
    
    def __init__(self, *args, **kwargs):
        super(CheckableCombo, self).__init__(*args, **kwargs)
        self._blockToggle = False
        self._lastEventTarget = None
        self.setModel(MultiComboBoxModel(self))
        self.model().checkStateChanged.connect(self.__updateCheckedItems)
        self.model().rowsInserted.connect(self.__updateCheckedItems)
        self.model().rowsRemoved.connect(self.__updateCheckedItems)
        self.activated[int].connect(self.__toggleCheckState)
        self.scrollFocus = False
        self.setLineEdit(QLineEdit())
        self.setInsertPolicy(QComboBox.NoInsert)
        self.setMinimumContentsLength(20)
        self.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
        
        self.view().installEventFilter(self)
        self.view().window().installEventFilter(self)
        self.view().viewport().installEventFilter(self)

    def checkedItems(self, data=False):
        """ Returns a list of checked item indexes
        """
        if self.model():
            currentIndex = self.model().index(0, self.modelColumn(), self.rootModelIndex())
            indexes = self.model().match(currentIndex, QtCore.Qt.CheckStateRole, QtCore.Qt.Checked, -1, QtCore.Qt.MatchExactly)
            if not data:
                return [str(index.data()) for index in indexes]
            else:
                return [self.itemData(index.row()) for index in indexes]
        return []

    def eventFilter(self, receiver, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self._lastEventTarget = type(receiver)
            # Cancel the dropdown persist if we've clicked outside the widget
            if receiver == self.view().window() and self.checkable and not type(receiver) == QFrame:
                self.hidePopup()
            return True

        elif event.type() == QtCore.QEvent.MouseButtonRelease and not type(receiver) == QFrame:
            try:
                self.itemClicked.emit(int(receiver.parent().currentIndex().row()))
            except:
                return False

        return False
        
    def showPopup(self):
        self._blockToggle = False
        super(CheckableCombo, self).showPopup()

    def hidePopup(self):
        if self.view().underMouse():
            pass
        else:
            self._blockToggle = True
            super(CheckableCombo, self).hidePopup()
            
    def __toggleCheckState(self, index):
        """ Toggles the check state for the supplied item index
        """
        if not self._blockToggle and self._lastEventTarget == QWidget:
            oldValue = self.itemData(index, QtCore.Qt.CheckStateRole)
            newValue = QtCore.Qt.Checked if (oldValue == QtCore.Qt.Unchecked) else QtCore.Qt.Unchecked
            self.setItemData(index, newValue, QtCore.Qt.CheckStateRole)

    def __updateCheckedItems(self):
        items = self.checkedItems()
        print items
        if items:
            self.setEditText(', '.join(items))
        else:
            self.setEditText('')

        self.selectionChanged.emit(items)

cb = CheckableCombo()
cb.addItem('Asd 1', 1)
cb.addItem('Asd 2', 2)
cb.show()