"""
NAME: Dim non-contributing nodes toggle
ICON: Icons/nodeDrag32x24.png
KEYBOARD_SHORTCUT: Ctrl+D
SCOPE:
This shelf script adds a keyboard shortcut to toggle the "Dim non-contributing nodes" preferences option.
Use 'Ctrl+D' to toggle the preference.

"""

KatanaPrefs[PrefNames.NODEGRAPH_DIMNONCONTRIBUTINGNODES] = not KatanaPrefs[PrefNames.NODEGRAPH_DIMNONCONTRIBUTINGNODES]
