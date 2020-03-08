import sys 
sys.path.append("C:\\Program Files\\FreeCAD 0.18\\bin") 
import FreeCAD
import random
import mdjrElements
from mdjrElements import *

levelHeight = 70

def mdjrMinarete(appClass, guiClass, draftClass, partClass, sketcherClass, counts, coords, bounds):
    classes = [appClass, guiClass, draftClass, partClass, sketcherClass]
    height = 0
    bodyCount = counts[0]
    baseSteps =  random.choice([[2,1],[1,2],[1,1,1],[1],[1,1]])
    for baseStep in baseSteps:
        cuarto(*classes,bounds[0],bounds[1],baseStep*levelHeight)
        draftClass.move([eval("appClass.ActiveDocument.Body"+'0'*(3-len(str(bodyCount)))+str(bodyCount))],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
        height += baseStep*levelHeight
        bodyCount += 1
    
    count = counts[1]
    for step in range(random.randint(3,5)):
        newBound = bounds[0] if bounds[0] < bounds[1] else bounds[1]
        minareteRotate(*classes, newBound*4/5,  levelHeight, 0)
        draftClass.move([eval("appClass.ActiveDocument.Fusion001"+'0'*(3-len(str(count)))+str(count))],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
        height += levelHeight
        count += 1
    
    roof = random.randint(15,25)/10
    minareteRotate(*classes, newBound*4/5,  levelHeight, levelHeight/5, roofFactor=roof)
    draftClass.move([eval("appClass.ActiveDocument.Fusion001"+'0'*(3-len(str(count)))+str(count))],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
    height += levelHeight*6/5
    count += 1
    
    newBound = newBound*4/5/roof
    for step in range(random.randint(0,2)):
        minareteRotate(*classes, newBound,  levelHeight*3/5, 0, windowType='pointed')
        draftClass.move([eval("appClass.ActiveDocument.Fusion001"+'0'*(3-len(str(count)))+str(count))],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
        height += levelHeight*3/5
        count += 1
        
    minareteRotate(*classes, newBound,  levelHeight*3/5, levelHeight*3/5, roofFactor=10, windowType='pointed')
    draftClass.move([eval("appClass.ActiveDocument.Fusion001"+'0'*(3-len(str(count)))+str(count))],appClass.Vector(coords[0],coords[1],coords[2]+height),copy=False)
    height += levelHeight*3/5
    count += 1
    
    return [bodyCount, count]

def mdjrCuarto(appClass, guiClass, draftClass, partClass, sketcherClass, counts, width, length, height):
    cuarto(appClass, guiClass, draftClass, partClass, sketcherClass, width, length, height)
    return [counts[0]+1,counts[1]]