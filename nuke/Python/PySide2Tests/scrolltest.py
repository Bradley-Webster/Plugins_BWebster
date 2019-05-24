import nukescripts
try:
    from PySide2 import QtWidgets
except:
    from PySide import QtGui as QtWidgets

class ScrollTestWidget(QtWidgets.QWidget):
    def __init__(self):
        super( ScrollTestWidget, self).__init__()
        self.setLayout( QtWidgets.QVBoxLayout() )
        self.myTable = QtWidgets.QTableWidget()
        for x in range(50):
            self.myTable.insertRow(x)
            self.myTable.setItem(x , 0, QtWidgets.QTableWidgetItem())
        self.layout().addWidget(self.myTable)

    def makeUI(self):
        self.scrollWidget = ScrollTestWidget()
        return self.scrollWidget

class ScrollTestPanel(nukescripts.PythonPanel):

  def __init__(self):
    super(ScrollTestPanel, self).__init__("ScrollTest", "ScollTest.id")
    self.scrollTestKnob = nuke.PyCustom_Knob( "scrolltest", "", "ScrollTestWidget()" )
    self.addKnob( self.scrollTestKnob )

menu = nuke.menu('Pane')
menu.addCommand('Scroll Test', lambda: ScrollTestPanel().addToPane())
nukescripts.registerPanel("ScollTest.id", lambda: ScrollTestPanel().addToPane())
