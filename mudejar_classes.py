import sys 
sys.path.append("C:\\Program Files\\FreeCAD 0.18\\bin") 
import FreeCAD
import numpy as np

def cubeVertices(appClass,l,w,h,origin=[0,0]):
    vertices = []
    vertices.append(origin)
    vertices.append([origin[0]+l,origin[1]])
    vertices.append([origin[0]+l,origin[1]+w])
    vertices.append([origin[0],origin[1]+w])
    appClass.Console.PrintMessage("good")
    return vertices

def sketchPolygon(appClass, partClass, sketcherClass, name, startN, *coordinates, isClosed=True):
    geoList = []
    for i, coordinate in enumerate(coordinates):
        cooNext = coordinates[(i+1)%len(coordinates)]
        geoList.append(partClass.LineSegment(appClass.Vector(coordinate[0],coordinate[1],0),
                                        appClass.Vector(cooNext[0],cooNext[1],0)))
    if not isClosed:
        geoList.pop()
    eval("appClass.ActiveDocument."+name).addGeometry(geoList,False)
    conList = []
    for i in range(startN,startN+len(coordinates)-(0 if isClosed else 2)):
        conList.append(sketcherClass.Constraint('Coincident',i,2,(i-startN+1)%len(coordinates)+startN,1))
    eval("appClass.ActiveDocument."+name).addConstraint(conList)
    appClass.ActiveDocument.recompute()

def sketchSpline(appClass, partClass, sketcherClass, name, startN, *coordinates, isClosed=False):
    coordinateVectors = []
    for coordinate in coordinates:
        coordinateVectors.append(FreeCAD.Vector(*coordinate))
    thisSketch = eval("appClass.activeDocument()."+name)
    thisSketch.addGeometry(partClass.Circle(coordinateVectors[0],appClass.Vector(0,0,1),10),True)
    thisSketch.addConstraint(sketcherClass.Constraint('Radius',startN,10.000000)) 
    for i in range(1,len(coordinates)):
        thisSketch.addGeometry(partClass.Circle(coordinateVectors[i],appClass.Vector(0,0,1),10),True)
        thisSketch.addConstraint(sketcherClass.Constraint('Equal',startN,startN+i))
    thisSketch.addGeometry(partClass.BSplineCurve(coordinateVectors,None,None,isClosed,3,None,False),False)
    conList = []
    for i in range(len(coordinates)):
        conList.append(sketcherClass.Constraint('InternalAlignment:Sketcher::BSplineControlPoint',i+startN,3,len(coordinates)+startN,i))
    thisSketch.addConstraint(conList)
    thisSketch.exposeInternalGeometry(startN+len(coordinates))

def padFromSketch(appClass, body, sketch, name, height, l2=100, reversePad=False, typePad=0):
    body.newObject("PartDesign::Pad",name)
    thisSketch = eval("appClass.activeDocument()."+name)
    thisSketch.Profile = sketch
    thisSketch.Length = 10.0
    appClass.ActiveDocument.recompute()
    appClass.ActiveDocument.recompute()
    thisSketch.Length = height
    thisSketch.Length2 = l2
    thisSketch.Type = typePad
    thisSketch.UpToFace = None
    thisSketch.Reversed = reversePad
    thisSketch.Midplane = 0
    thisSketch.Offset = 0.000000
    appClass.ActiveDocument.recompute()
    
def pocketFromSketch(appClass, body, sketch, name, height, reversePocket=False, midPlane=0):
    body.newObject("PartDesign::Pocket",name)
    thisSketch = eval("appClass.activeDocument()."+name)
    thisSketch.Profile = sketch
    thisSketch.Length = 10.0
    appClass.ActiveDocument.recompute()
    appClass.ActiveDocument.recompute()
    thisSketch.Length = height
    thisSketch.Length2 = 100.000000
    thisSketch.Type = 0
    thisSketch.UpToFace = None
    thisSketch.Reversed = reversePocket
    thisSketch.Midplane = midPlane
    thisSketch.Offset = 0.000000
    appClass.ActiveDocument.recompute()

def pointedArch(appClass, partClass, sketcherClass, name, startN, bottomLeft, height, width):
    sketchPolygon(appClass,partClass,sketcherClass,name,startN,
                  (bottomLeft[0]+width,bottomLeft[1]+height/3),
                  (bottomLeft[0]+width,bottomLeft[1]),
                  (bottomLeft[0],bottomLeft[1]),
                  (bottomLeft[0],bottomLeft[1]+height/3),isClosed=False)
    sketchSpline(appClass,partClass,sketcherClass,name,startN+3,
                 (bottomLeft[0],bottomLeft[1]+height/3),
                 (bottomLeft[0],bottomLeft[1]+2*height/3),
                 (bottomLeft[0]+width/2,bottomLeft[1]+height),isClosed=False)
    sketchSpline(appClass,partClass,sketcherClass,name,startN+9,
                 (bottomLeft[0]+width/2,bottomLeft[1]+height),
                 (bottomLeft[0]+width,bottomLeft[1]+2*height/3),
                 (bottomLeft[0]+width,bottomLeft[1]+height/3),isClosed=False)
    thisSketch = eval("appClass.activeDocument()."+name)
    thisSketch.addConstraint(sketcherClass.Constraint('Coincident',startN+6,1,startN+2,2)) 
    thisSketch.addConstraint(sketcherClass.Constraint('Coincident',startN+6,2,startN+12,1)) 
    thisSketch.addConstraint(sketcherClass.Constraint('Coincident',startN+12,2,startN,1)) 

def lobedArch(appClass, partClass, sketcherClass, name, startN, bottomLeft, height, width):
    sketchPolygon(appClass,partClass,sketcherClass,name,startN,
                  (bottomLeft[0]+width,bottomLeft[1]+height/2),
                  (bottomLeft[0]+width,bottomLeft[1]),
                  (bottomLeft[0],bottomLeft[1]),
                  (bottomLeft[0],bottomLeft[1]+height/2),isClosed=False)
    thisSketch = eval("appClass.activeDocument()."+name)
    thisSketch.addGeometry(partClass.ArcOfCircle(partClass.Circle(appClass.Vector(bottomLeft[0]+width/4,bottomLeft[1]+height/2,0),
                                                                       appClass.Vector(0,0,1),width/4),3.1415926535/2,3.1415926535),False)
    thisSketch.addGeometry(partClass.ArcOfCircle(partClass.Circle(appClass.Vector(bottomLeft[0]+width/2,bottomLeft[1]+height/2+width/4,0),
                                                                  appClass.Vector(0,0,1),width/4),0,3.1415926535),False)
    thisSketch.addGeometry(partClass.ArcOfCircle(partClass.Circle(appClass.Vector(bottomLeft[0]+3*width/4,bottomLeft[1]+height/2,0),
                                                                  appClass.Vector(0,0,1),width/4),0,3.1415926535/2),False)
    thisSketch.addConstraint(sketcherClass.Constraint('Coincident',startN+3,2,startN+2,2)) 
    thisSketch.addConstraint(sketcherClass.Constraint('Coincident',startN+4,2,startN+3,1)) 
    thisSketch.addConstraint(sketcherClass.Constraint('Coincident',startN+4,1,startN+5,2)) 
    thisSketch.addConstraint(sketcherClass.Constraint('Coincident',startN+5,1,startN,1))