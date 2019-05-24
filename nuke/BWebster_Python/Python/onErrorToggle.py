'''
Name: onErrorToggle.py
Created by: Bradley Webster

Description:
    Toggles Read nodes with missing frames between black and nearest frame
'''

import nuke


def toggleError():
    n = nuke.allNodes()
    s = nuke.selectedNodes()

    # If nodes are selected, use them, if not scan all nodes.
    if s == []:
        s = n

    for i in s:
        if i.Class() == "Read":
            on_error = i.knob("on_error").getValue()
            # Toggles between black and nearest frame
            if on_error == 3:
                i.knob("on_error").setValue('1')
            else:
                i.knob("on_error").setValue('3')
