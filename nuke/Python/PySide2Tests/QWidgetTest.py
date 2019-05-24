from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

nuke.tprint('testlaunch')
obvious exception
def get_main_window():
    window_name = 'Foundry::UI::DockMainWindow'

    for w in QApplication.topLevelWidgets():
        if w.inherits('QMainWindow') and window_name in w.metaObject().className():
            nuke.tprint( 'yes')
            return w
    nuke.tprint('no')

    return None


class MainWindow(QMainWindow):
    def __init__(self, parent=get_main_window()):
        super(MainWindow, self).__init__(parent)


get_main_window()
