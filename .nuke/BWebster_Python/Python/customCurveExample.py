'''
Name: customCurveExample.py
Created by: Bradley Webster

Description: Creates a Constant with a preset curve
             Used as an example of curves with sloped values
             Q100387: Using Python to set keyframes and adjust slopes
'''

import nuke

# Add Curve Data into the script
# x: { y, bezier}
# Curve data stored in dictionary object
curve_data = {1: {'val': 1, 'in_slope': 0.0},
              30: {'val': 10, 'in_slope': 0.0},
              50: {'val': 5, 'in_slope': -56.957},
              60: {'val': 0, 'in_slope': -14.341},
              70: {'val': 5, 'in_slope': 56.957},
              80: {'val': 5, 'in_slope': -77.891},
              90: {'val': 5, 'in_slope': 0.0}}


def create_curve(curve_data):
    # Create a Constant node to add slope
    constantNode = nuke.createNode('Constant')

    # Get the 'Color' knob out of the Constant node
    colorKnob = constantNode['color']

    # Set the knob to enabled so multiple keys can be added
    colorKnob.setAnimated()

    # For each dictionary object, set a key in the curve
    # This value needs to be added before colorKnob.animations() can be called
    for frame, key in sorted(curve_data.items()):
        colorKnob.setKeyAt(frame)

    # Set up the keys in an object to be called later
    curve = colorKnob.animations()[0]
    keys = curve.keys()

    # Index for each dictionary object used in loop
    index = 0

    # Loop the dictionary, for each entry add the curve data
    for frame, key in sorted(curve_data.items()):
        # Current key to add dictionary curve information
        frameKey = keys[index]

        val = key['val']
        in_slope = key['in_slope']

        # Add curve data to the key
        # In this example, we would like both tangents to be the same
        # so in_slope is used for both the lslope and rslope values
        frameKey.lslope = in_slope
        frameKey.rslope = in_slope
        frameKey.y = val

        # Append the frameKey to the next added frame
        index += 1

    # Set the interpolation of the curve to the user created Bezier
    # If you are not using user created Beziers, you can use the following instead (CONSTANT, LINEAR, SMOOTH, CATMULL_ROM, cubic)
    curve.changeInterpolation(keys, nuke.USER_SET_SLOPE)

# Call the definition to initialize the script
create_curve(curve_data)

