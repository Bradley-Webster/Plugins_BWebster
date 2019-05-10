"""
NAME: autokeyEnableCurvesExample
ICON: Icons/showCurveOn.png
KEYBOARD_SHORTCUT:
SCOPE: This example script will create an auto Translation curve for a PrimitiveCreate node and enable the Curve via ParameterPolicies

"""

def addTranslateYCurve():
    # Get the root node
    rootNode = NodegraphAPI.GetRootNode()

    # Create a new node under the root node

    primNode = NodegraphAPI.CreateNode('PrimitiveCreate', rootNode)

    # Get the Translate Y parameter from a PrimitiveCreate node
    translateY = NodegraphAPI.GetNode('PrimitiveCreate').getParameter('transform.translate.y')

    # Set a few keys
    translateY.setAutoKey(True)
    # Height 25 at Frame 1
    translateY.setValueAutoKey(0, 1)
    # Height 50 at Frame 50
    translateY.setValueAutoKey(20, 50)
    # Height 0 at Frame 100
    translateY.setValueAutoKey(0, 100)

    # Create new ParameterPolicy
    myParameterPolicy = UI4.FormMaster.CreateParameterPolicy(None, translateY)

    # Enable Animation curves
    myParameterPolicy.setCurveEnabled(True)
    myParameterPolicy.setCurveViewed(True)

addTranslateYCurve()
