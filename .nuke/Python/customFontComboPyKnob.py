from PySide2 import QtWidgets, QtCore
import nuke

class customFontComboPyKnob(QtWidgets.QFontComboBox):

    def __init__(self, node):
        super(self.__class__, self).__init__()
        fontFilters = self.fontFilters()
        #each knob will need a custom name
        self.name=node.name()

    #Needed by Nuke to add the widget
    def makeUI(self):
        return self

    def updateValue(self):
        pass


def addPySideFontKnob():
    addKnob = customFontComboPyKnob()


nuke.addOnScriptLoad(addPySideFontKnob)

