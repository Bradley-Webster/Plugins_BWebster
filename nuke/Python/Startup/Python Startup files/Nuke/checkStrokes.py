import nuke.rotopaint as rp

def getStrokes(layer):
    strokes = []
    for element in layer:
        if isinstance(element, nuke.rotopaint.Layer):
            strokes.extend(getStrokes(element))
        elif isinstance(element, nuke.rotopaint.Stroke):
            strokes.append(element)
    return strokes

def updateElements():
    knob = nuke.thisKnob()
    node = nuke.thisNode()
    if knob.name() == 'curves':
        strokes = getStrokes(knob.rootLayer)
        elements = ''
        lenOldElements = 0
    for stroke in strokes:
        elements = elements + stroke.name + ','
        elements = elements[:-1]
        oldElements = node['elements'].value().split(',')
        if oldElements[0] == '':
            lenOldElements = 0
        else:
            lenOldElements = len(oldElements)
            print lenOldElements
    if lenOldElements >= len(strokes):
        print 'No new strokes'
        node['elements'].setValue(elements)
        return
    else:
        for stroke in strokes:
            if stroke.name not in oldElements:
                print 'New Stroke: ' + stroke.name
