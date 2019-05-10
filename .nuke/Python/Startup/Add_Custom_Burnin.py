from hiero.core import events

def addCustomBurnin():
    from hiero.ui import registerAction
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QAction
    import nuke
    nuke.load ("LL_BurnIn_Hiero")
    action = QAction(QIcon("icons:LUT.png"), "LL_BurnIn_Hiero", None)
    action.setObjectName("foundry.timeline.effect.LL_BurnIn_Hiero")
    action.setToolTip("LL_BurnIn_Hiero for Nuke Studio")
    action.setData("LL_BurnIn_Hiero")
    registerAction(action)

events.registerInterest("kStartup", eventCallback)
