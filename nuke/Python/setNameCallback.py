import nuke

def NameChanged():
    n = nuke.thisNode()
    nALL = nuke.allNodes()
    k = nuke.thisKnob()
    for nodes in nALL:
        if nodes != n:
            if k.name() == "name":
                otherName = nodes.knob("name").getValue()
                if k.getText() == otherName :
                    newMessage = k.getText() + ' already exists, Nuke will auto label Node to next available addition. '
                    nuke.message(str(newMessage))

nuke.addKnobChanged(NameChanged)

