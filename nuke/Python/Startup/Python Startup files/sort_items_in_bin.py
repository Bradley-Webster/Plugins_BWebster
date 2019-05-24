import hiero.core
import hiero.ui
from functools import partial

# Set up PySide, create exception for PySide2 (for Nuke11+ scripts)
try:
    from PySide import QtGui, QtCore
    from PySide.QtGui import *
    from PySide.QtCore import *
except ImportError:
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *


# CustomContextMenuTest Class for Menu and actions
class sort_items_in_bin(object):

    def __init__(self):
        hiero.core.events.registerInterest('kShowContextMenu/kBin', self.event_handler)

    def event_handler(self, event):
        self._selection = event.sender.selection()

        if len(self._selection) > 0:
            self._action = QAction('Sort Items in Bin', None)
            self._action.triggered.connect(self.sort_it)

            self._raction = QAction('Sort Items in Bin Recursively', None)
            self._raction.triggered.connect(partial(self.sort_it, True))

            for action in event.menu.actions():
                if str(action.text()) == 'Edit':
                    self._action.setShortcut('Ctrl+R')
                    self._raction.setShortcut('Ctrl+Shift+R')
                    # Add action UI
                    action.menu().addAction(self._action)
                    action.menu().addAction(self._raction)
                    # Add keyboard shortcut
                    hiero.ui.mainWindow().addAction(self._action)
                    hiero.ui.mainWindow().addAction(self._raction)
                    break

    def sort_it(self, recursive=False):

        for s in self._selection:
            self.sort_items_in_bin(s, recursive)

    def _name_dict(self, elements):
        '''returns dict of elements with unique name as key and element as value
        @param elements tuple or list of elements
        '''

        edict = {}
        for i, e in enumerate(elements):
            edict.update({ e.name()+str(i) : e })
        return(edict)

    def sort_items_in_bin(self, bin, recursive=False):
        '''removes all items of bin and adds them sorted
        @param bin bin object
        @param recursive bool whether to sort also items that are bins
        '''

        items = bin.items()
        versionItems = [i for i in items if isinstance(i, hiero.core.Version)]

        if versionItems != []:
            print 'test'
            bin = versionItems[0].parent().parentBin()
            items = bin.items()

        for i in bin.items():
            bin.removeItem(i)

        if recursive == True:
            binitems = [i for i in items if isinstance(i, hiero.core.Bin)]
            for b in binitems:
                self.sort_items_in_bin(b, recursive=recursive)

        itemdict = self._name_dict(items)
        for i in sorted(itemdict.keys()):
            bin.addItem(itemdict[i])

sort_items_in_bin()
