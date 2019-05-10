def insertKnob(node, newKnob, targetKnob, beforeOrAfter='before'):
    """
    Add new node either before or after targeted node

    :param node:
    :param newKnobName: ( New Node Name)
    :param newKnobLabel: ( New Node Label )
    :param targetKnob:  ( Targeted node )
    :param beforeOrAfter:  (Optional, will use 'before' if nothing added)
    """

    # Add local indexing variables
    user_knob_index = 0
    knobIndex = 0
    knobFound = False

    # Find out where the "User Tab" is, this is the start of user knobs
    for knobs in node.allKnobs():
        if knobs.name() == 'User':
            break
        user_knob_index += 1

    user_knobs = node.allKnobs()[(user_knob_index + 1):]

    # Check if targeted knob exists, use index for later insertion
    for knob in user_knobs:
        if knob.name() == targetKnob:
            knobFound = True
            break
        else:
            knobIndex += 1

    # If targeted knob exists, continue
    if knobFound == True:
        # Remove all current knobs in user tab ( This will NOT delete added variables )
        for knob in user_knobs:
            node.removeKnob(knob)

        # Add knob before or after the targeted knob
        if beforeOrAfter == 'before':
            user_knobs.insert(knobIndex, newKnob)
        else:
            user_knobs.insert(knobIndex+1, newKnob)

        # Add knobs back to node
        for knob in user_knobs:
            node.addKnob(knob)

        print 'New knob added successfully'

    # No targeted knob found, exit snippet
    else:
        print 'Chosen knob does not exist, exiting'


# Node to add new user knob
node = nuke.selectedNode()

# New knob to be added
newKnobName = 'insertedKnob'
newKnobLablel = 'newKnobBefore'
newKnob = nuke.Double_Knob( newKnobName, newKnobLabel )

# Main function
insertKnob(node, newKnob, 'firstKnob', 'before')


