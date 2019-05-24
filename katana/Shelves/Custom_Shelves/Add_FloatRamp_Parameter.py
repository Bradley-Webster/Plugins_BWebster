"""
NAME: addFloatRampParameter
ICON: Icons/showCurveOn.png
KEYBOARD_SHORTCUT:
SCOPE:
Created by Bradley Webster - Foundry Customer Support

Add floatRamp to selected Node

The floatRamp will be given custom values displayed within the source

"""

def __addFloatRampParameter(floatNode):
    """
    Adds a group parameter containing four child parameters to the node
    that define a float ramp.  (floatRamp, rampSize, positionsArray, valuesArray')
    """
    # Set up names of child parameters
    rootparm = floatNode.getParameters()
    positionsParameterName = 'positions'
    valuesParameterName = 'values'
    interpolatorParameterName = 'interp'

    # Create a group parameter as the main parameter of the float ramp
    floatRampGroupParam = rootparm.createChildGroup('floatRamp')
    floatRampGroupParam.setHintString(repr({
        'widget': 'floatRamp',
        'rampKnots': positionsParameterName,
        'rampFloats': valuesParameterName,
        'rampInterp': interpolatorParameterName}))

    # Create a child number parameter for setting the number of knots (+2)
    rampSize = floatRampGroupParam.createChildNumber('rampSize', 5)
    rampSize.setHintString(repr({"widget": "null", "type": "int"}))

    # Create child number parameters for the ramp positions (Knots)(X Graph value)
    positionsArray = floatRampGroupParam.createChildNumberArray(
        positionsParameterName, 5)
    positionsArray.setHintString(repr({"isDynamicArray": "1", "widget": "null", "size": "6", "type": "float", "default": "0.0, 0.5, 1.0"}))

    # Edit Positions of indexes (Knots)(X Graph value)
    positionsArray.getChildByIndex(0).setValue(0, 0)
    positionsArray.getChildByIndex(1).setValue(0, 0)
    positionsArray.getChildByIndex(2).setValue(0.5, 0)
    positionsArray.getChildByIndex(3).setValue(1, 0)
    positionsArray.getChildByIndex(4).setValue(1, 0)

    # Create child number parameters for the ramp values (Floats)(Y Graph value)
    valuesArray = floatRampGroupParam.createChildNumberArray(
        valuesParameterName, 5)
    valuesArray.setHintString(repr({"isDynamicArray": "1", "widget": "null", "size": "6", "type": "float", "default": "0.0, 0.5, 1.0"}))

    # Edit Values of indexes (Floats)(Y Graph value)
    valuesArray.getChildByIndex(0).setValue(0, 0)
    valuesArray.getChildByIndex(1).setValue(0, 0)
    valuesArray.getChildByIndex(2).setValue(0.5, 0)
    valuesArray.getChildByIndex(3).setValue(1, 0)
    valuesArray.getChildByIndex(4).setValue(1, 0)
    # Create a child string parameter for defining the interpolator to use
    interpolation  = floatRampGroupParam.createChildString(
        interpolatorParameterName, 'linear')
    interpolation .setHintString(repr({"widget": "null", "default": "linear", "options": "linear|catmull-rom|bspline|bezier"}))

    return floatRampGroupParam

# Get or Create your Node to add Float Ramp
allSelected = NodegraphAPI.GetAllSelectedNodes()
floatNode = allSelected[0]

# Add Float Ramp to your selected Node
__addFloatRampParameter(floatNode)
