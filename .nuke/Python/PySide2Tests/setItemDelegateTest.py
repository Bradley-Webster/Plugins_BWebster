try:

    from PySide2 import QtWidgets, QtCore

except(ImportError):

    from PySide import QtCore

    from PySide import QtGui as QtWidgets



class MyDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):

        super(MyDelegate, self).__init__(parent)



    def paint(self, painter, option, index):

        painter.drawText(option.rect,

                         index.data())



class MyModel(QtCore.QAbstractTableModel):

    def __init__(self, node_list, parent=None):

        super(MyModel, self).__init__(parent)

        self.setNodes(node_list)



    def setNodes(self, node_list):

        self.nodes = node_list



    def data(self, index, role):

        return self.nodes[index.row()].name()



    def columnCount(self, index=None):

        return 3



    def rowCount(self, index=None):

        return len(self.nodes)



v = QtWidgets.QTableView()

model = MyModel(["hey","there","world"])

v.setModel(model)



v.setItemDelegateForColumn(0, MyDelegate())



# Workaround 

#v.setItemDelegate(MyDelegate())



v.show()
