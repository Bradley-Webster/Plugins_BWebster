"""
NAME: Not Tetris
ICON: Icons/Timebar/launch_hilite20.png
KEYBOARD_SHORTCUT: Ctrl+Shift+T
SCOPE:
Open the Hydra Viewer and open the shelf for surprise!

Please Keep Internal... :)

"""

viewerTab = UI4.App.Tabs.FindTopTab('Viewer (Hydra)')
delegate = viewerTab.getViewerDelegateByIndex(0)
name = delegate.getViewportName(0)
vpw = viewerTab.getViewportWidget(name, delegate)
vpw.addLayer("TetrominoLayer", "Tetris")
