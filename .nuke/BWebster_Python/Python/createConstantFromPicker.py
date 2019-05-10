'''
Name: createConstantFromPicker.py
Created by: Bradley Webster

Description: Creates a Constant from the Color Picker's currently set color value

'''

import nuke

try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore


def getColor():
    import hiero
    for window in hiero.ui.windowManager().windows():
        if window.windowTitle() == "Pixel Analyzer":
            pixelAnalyzer = window
            break
    
    buttons = pixelAnalyzer.findChildren(QtWidgets.QPushButton)
    # Need to select the "average" color sample to update the values in the QLineEdits 
    # TODO restore the original selection after
    buttons[3].click()

    lineEdits = pixelAnalyzer.findChildren(QtWidgets.QLineEdit)
    # The first 4 QLineEdits contain the rgba values
    r = float(lineEdits[0].text())
    g = float(lineEdits[1].text())
    b = float(lineEdits[2].text())
    a = float(lineEdits[3].text())
    return r, g, b, a

def createConstant():
    x= nuke.nodes.Constant()
    x["color"].setValue(getColor())
