import hiero.ui
import nuke
import sys
import os

if nuke.env['NukeVersionMajor'] >= 11:
  from PySide2.QtGui import QIcon
  from PySide2.QtWidgets import QAction
else:
  from PySide.QtGui import QIcon, QAction

from hiero.ui import registerAction

# This creates an action with an icon and effect named "Gain Control"
action = QAction(QIcon("icons:LUT.png"), "Test", None)

# Soft effect actions can be found by prefixing the QAction's objectName with: 'foundry.timeline.effect'
action.setObjectName("foundry.timeline.effect.addBlinkScript")

# Setting of Data here will point to the Nuke node class name.
action.setData("BlinkScript")
print action.data().toString()
# This registers your custom action with the Effects Menu
registerAction(action)
