import nuke
import editWriteNodes

menubar=nuke.menu("Nuke")

m=menubar.addMenu("&Custom")

m.addCommand("&Edit Comp File Formats", lambda: editWriteNodes.editCompsUI(), "Ctrl+Shift+e")




