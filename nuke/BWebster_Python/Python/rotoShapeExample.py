'''
Name: RotoShape Python Example
Version: 1.0
Created by: Bradley Webster

Description:
    Quick RotoShape triangle example with Python

'''
import nuke.rotopaint as rp

def pythonRotoExample():
    roto_node = nuke.nodes.Roto()

    curvesKnob = roto_node["curves"]

    shape = rp.Shape(curvesKnob)
    shape.name = "myShape1"

    point = rp.ShapeControlPoint(100, 100)
    shape.append(point)
    point = rp.ShapeControlPoint(500, 100)
    shape.append(point)
    point = rp.ShapeControlPoint(100, 500)
    shape.append(point)

    curvesKnob.rootLayer.append(shape)
