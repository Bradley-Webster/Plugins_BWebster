import os
import re

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
    
class Transcode_Attr(QWidget):
    def init(self):
        QWidget.init(self)
    def show_ui(self):
       self.show()

ui = Transcode_Attr()
ui.show_ui()
