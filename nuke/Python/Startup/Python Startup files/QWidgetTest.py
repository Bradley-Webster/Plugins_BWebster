import nuke

if nuke.NUKE_VERSION_MAJOR >= 11:
	from PySide2.QtWidgets import *
        from PySide2.QtGui import *
        from PySide2.QtCore import *

else:
        from PySide.QtGui import *
        from PySide.QtCore import *

def get_main_window():
    window_name = 'Foundry::UI::DockMainWindow'

    for w in QApplication.topLevelWidgets():
        if w.inherits('QMainWindow') and window_name in w.metaObject().className():
            return w
    return None

class MainWindow(QMainWindow):
    def __init__(self, parent=get_main_window()):
        super(MainWindow, self).__init__(parent)
