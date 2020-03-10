import sys 
sys.path.append("C:\\Program Files\\FreeCAD 0.18\\bin") 
import FreeCAD
import random
import mdjrElements
from mdjrElements import *

levelHeight = 75

def mdjrMinarete(appClass, guiClass, draftClass, partClass, sketcherClass, sides, coords, bounds):
    classes = [appClass, guiClass, draftClass, partClass, sketcherClass]
    height = 0
    baseSteps =  random.choice([[2,1],[1,2],[1,1,1],[1],[1,1]])
    for baseStep in baseSteps:
        cuarto(*classes,bounds[0],bounds[1],baseStep*levelHeight)
        draftClass.move([appClass.ActiveDocument.Objects[-1]],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
        height += baseStep*levelHeight
    
    for step in range(random.randint(3,5)):
        newBound = bounds[0] if bounds[0] < bounds[1] else bounds[1]
        minareteRotate(*classes, newBound*4/5,  levelHeight, 0, sides)
        draftClass.move([appClass.ActiveDocument.Objects[-1]],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
        height += levelHeight
    
    roof = random.randint(15,25)/10
    minareteRotate(*classes, newBound*4/5,  levelHeight, levelHeight/5, sides, roofFactor=roof)
    draftClass.move([appClass.ActiveDocument.Objects[-1]],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
    height += levelHeight*6/5
    
    newBound = newBound*4/5/roof
    for step in range(random.randint(0,2)):
        minareteRotate(*classes, newBound,  levelHeight*3/5, 0, sides, windowType='pointed')
        draftClass.move([appClass.ActiveDocument.Objects[-1]],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
        height += levelHeight*3/5
        
    minareteRotate(*classes, newBound,  levelHeight*3/5, levelHeight*3/5, sides, roofFactor=10, windowType='pointed')
    draftClass.move([appClass.ActiveDocument.Objects[-1]],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
    height += levelHeight*3/5

def mdjrCuarto(appClass, guiClass, draftClass, partClass, sketcherClass, counts, coords, width, length, height):
    cuarto(appClass, guiClass, draftClass, partClass, sketcherClass, width, length, height)
    draftClass.move([appClass.ActiveDocument.Objects[-1]],appClass.Vector(*coords),copy=False)
    return [counts[0]+1,counts[1]]