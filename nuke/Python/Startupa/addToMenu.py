
try:
    import sys
    import nuke
    import hiero.core
    from PySide2 import QtGui, QtWidgets
    import text_and_transform as tt
except Exception, e:
    print __file__, " could not import correctly:", str(e)
else:

    menubar = hiero.ui.menuBar()

    m = None
    mas = menubar.actions()
    for ma in mas:
        if ma.text() == "&BlueBolt":
            m = ma.menu()

    if m:
        m = m.addMenu("Editorial")
    else:
        m = menubar.addMenu("&BlueBolt")

    createProjectAction = QtWidgets.QAction(QtGui.QIcon(''), "Create Project", None)
    createProjectAction.triggered.connect(tt.createProject)
    m.addAction(createProjectAction)

    addColorspaceAction = QtWidgets.QAction(QtGui.QIcon(''), "Apply Colorspace", None)
    addColorspaceAction.triggered.connect(tt.toggleColorspace)
    addColorspaceAction.setShortcut(QtGui.QKeySequence('Alt+C'))
    m.addAction(addColorspaceAction)

    addInfoStripOnlyAction = QtWidgets.QAction(QtGui.QIcon(''), "Toggle Top Left Info Strip", None)
    addInfoStripOnlyAction.triggered.connect(tt.addTopLeftInfoStrip)
    addInfoStripOnlyAction.setShortcut(QtGui.QKeySequence('Alt+T'))
    m.addAction(addInfoStripOnlyAction)

    addBottomLeftInfoStripOnlyAction = QtWidgets.QAction(QtGui.QIcon(''), "Toggle Bottom Right Info Strip", None)
    addBottomLeftInfoStripOnlyAction.triggered.connect(tt.addBottomLeftInfoStrip)
    addBottomLeftInfoStripOnlyAction.setShortcut(QtGui.QKeySequence('Alt+Shift+T'))
    m.addAction(addBottomLeftInfoStripOnlyAction)

    toggleHardMaskAction = QtWidgets.QAction(QtGui.QIcon(''), "Toggle Hard Mask", None)
    toggleHardMaskAction.triggered.connect(tt.toggleHardMask)
    toggleHardMaskAction.setShortcut(QtGui.QKeySequence('M'))
    m.addAction(toggleHardMaskAction)
