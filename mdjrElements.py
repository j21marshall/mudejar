import sys 
sys.path.append("C:\\Program Files\\FreeCAD 0.18\\bin") 
import FreeCAD
import numpy as np
import mudejar_classes
from mudejar_classes import *

def minareteSlice(appClass, guiClass, draftClass, partClass, sketcherClass, octSide, octSlice, height, roofHeight, roofFactor, winType):
    guiClass.activateWorkbench("DraftWorkbench")
    appClass.activeDocument().addObject('PartDesign::Body','Body')

    appClass.activeDocument().Body.newObject('Sketcher::SketchObject','Sketch')
    appClass.activeDocument().Sketch.Support = (appClass.activeDocument().XZ_Plane, [''])
    appClass.activeDocument().Sketch.MapMode = 'FlatFace'
    appClass.ActiveDocument.recompute()

    sketchPolygon(appClass,partClass,sketcherClass,"Sketch",0,(-octSlice/2,0),(-octSlice/2,height),(-octSlice/2/roofFactor,height+roofHeight),(octSlice/2/roofFactor,height+roofHeight),(octSlice/2,height),(octSlice/2,0))
    sketchPolygon(appClass,partClass,sketcherClass,"Sketch",6,(-(octSlice/2-4),4),(-(octSlice/2-4),height-4),(octSlice/2-4,height-4),(octSlice/2-4,4))

    padFromSketch(appClass,appClass.activeDocument().Body,appClass.activeDocument().Sketch,"Pad",octSide/2,l2=octSide/2,typePad=4)
    guiClass.activeDocument().hide("Sketch")
    guiClass.activeDocument().hide("Pad")

    if winType != 'none':
        appClass.activeDocument().Body.newObject('Sketcher::SketchObject','SketchWindow')
        appClass.activeDocument().SketchWindow.Support = (appClass.activeDocument().YZ_Plane, [''])
        appClass.activeDocument().SketchWindow.MapMode = 'FlatFace'
        #appClass.ActiveDocument.recompute()

        if winType == 'pointed':
            pointedArch(appClass,partClass,sketcherClass,"SketchWindow",0,(-octSide/4,height/4),height/2,octSide/2)
        else:
            lobedArch(appClass,partClass,sketcherClass,"SketchWindow",0,(-octSide*3/8,height/4),height*3/4,octSide*3/4)

        pocketFromSketch(appClass,appClass.activeDocument().Body,appClass.activeDocument().SketchWindow,"Pocket",250,midPlane=1)
        guiClass.activeDocument().hide("SketchWindow")
        
        if winType != 'pointed':
            appClass.activeDocument().Body.newObject('Sketcher::SketchObject','SketchIn')
            appClass.activeDocument().SketchIn.Support = (appClass.activeDocument().XY_Plane, [''])
            appClass.activeDocument().SketchIn.MapMode = 'FlatFace'
            #appClass.ActiveDocument.recompute()

            sketchPolygon(appClass,partClass,sketcherClass,"SketchIn",0,(-octSlice/2+4,-octSide/2),(-octSlice/2+8,-octSide/2),(-octSlice/2+8,octSide/2),(-octSlice/2+4,octSide/2))
            sketchPolygon(appClass,partClass,sketcherClass,"SketchIn",4,(octSlice/2-4,-octSide/2),(octSlice/2-8,-octSide/2),(octSlice/2-8,octSide/2),(octSlice/2-4,octSide/2))

            padFromSketch(appClass,appClass.activeDocument().Body,appClass.activeDocument().SketchIn,"PadIn",height)
            guiClass.activeDocument().hide("SketchIn")
            guiClass.activeDocument().hide("PadIn")

            appClass.activeDocument().Body.newObject('Sketcher::SketchObject','SketchInWin')
            appClass.activeDocument().SketchInWin.Support = (appClass.activeDocument().YZ_Plane, [''])
            appClass.activeDocument().SketchInWin.MapMode = 'FlatFace'
            appClass.ActiveDocument.recompute()

            pointedArch(appClass,partClass,sketcherClass,"SketchInWin",0,(-octSide/8,height*3/8),height/4,octSide/4)

            pocketFromSketch(appClass,appClass.activeDocument().Body,appClass.activeDocument().SketchInWin,"PockInW",250,midPlane=1)
            guiClass.activeDocument().hide("SketchInWin")
            guiClass.activeDocument().hide("PockInW")

    appClass.activeDocument().Body.newObject('Sketcher::SketchObject','SketchRoof')
    appClass.activeDocument().SketchRoof.Support = (appClass.activeDocument().XY_Plane, [''])
    appClass.activeDocument().SketchRoof.MapMode = 'FlatFace'
    appClass.ActiveDocument.recompute()

    sketchPolygon(appClass,partClass,sketcherClass,"SketchRoof",0,(-octSlice/2,-octSide/2),(-octSlice/2/roofFactor,-octSide/2/roofFactor),(octSlice/2/roofFactor,-octSide/2/roofFactor),(octSlice/2,-octSide/2),
                  (octSlice/2,octSide/2),(octSlice/2/roofFactor,octSide/2/roofFactor),(-octSlice/2/roofFactor,octSide/2/roofFactor),(-octSlice/2,octSide/2))
    sketchPolygon(appClass,partClass,sketcherClass,"SketchRoof",8,(-octSide*4,-octSide*4),(-octSide*4,octSide*4),(octSide*4,octSide*4),(octSide*4,-octSide*4))

    pocketFromSketch(appClass,appClass.activeDocument().Body,appClass.activeDocument().SketchRoof,"PocketRoof",250,midPlane=1)
    guiClass.activeDocument().hide("SketchRoof")
    guiClass.activeDocument().hide("Pocket")

def minareteRotate(appClass, guiClass, draftClass, partClass, sketcherClass, width, height, roofHeight, roofFactor=2, windowType=''):
    octLongInSide = width
    octSide = octLongInSide/3**(1/2)
    minareteSlice(appClass, guiClass, draftClass, partClass, sketcherClass, octSide, octLongInSide, height, roofHeight, roofFactor, winType=windowType)

    activeDoc = appClass.ActiveDocument
    draftClass.clone(activeDoc.Body)
    draftClass.rotate([activeDoc.Clone],60.0,appClass.Vector(0,0,0),axis=appClass.Vector(0.0,0.0,1.0),copy=False)
    draftClass.clone(activeDoc.Body)
    draftClass.rotate([activeDoc.Clone001],120.0,appClass.Vector(0,0,0),axis=appClass.Vector(0.0,0.0,1.0),copy=False)

    activeDoc.addObject("Part::MultiFuse","Fusion")
    activeDoc.Fusion.Shapes = [appClass.activeDocument().Body,appClass.activeDocument().Clone,]
    guiClass.activeDocument().Body.Visibility=False
    guiClass.activeDocument().Clone.Visibility=False
    guiClass.ActiveDocument.Fusion.ShapeColor=guiClass.ActiveDocument.Body.ShapeColor
    guiClass.ActiveDocument.Fusion.DisplayMode=guiClass.ActiveDocument.Body.DisplayMode
    activeDoc.recompute()
    activeDoc.addObject("Part::MultiFuse","Fusion001")
    activeDoc.Fusion001.Shapes = [appClass.activeDocument().Clone001,appClass.activeDocument().Fusion,]
    guiClass.activeDocument().Clone001.Visibility=False
    guiClass.activeDocument().Fusion.Visibility=False
    guiClass.ActiveDocument.Fusion001.ShapeColor=guiClass.ActiveDocument.Clone001.ShapeColor
    guiClass.ActiveDocument.Fusion001.DisplayMode=guiClass.ActiveDocument.Clone001.DisplayMode
    activeDoc.recompute()
    activeDoc.addObject('Part::Feature','Fusion001').Shape=appClass.ActiveDocument.Fusion001.Shape.removeSplitter()
    activeDoc.ActiveObject.Label=appClass.ActiveDocument.Fusion001.Label
    guiClass.ActiveDocument.Fusion001.hide()

    guiClass.ActiveDocument.ActiveObject.ShapeColor=guiClass.ActiveDocument.Fusion001.ShapeColor
    guiClass.ActiveDocument.ActiveObject.LineColor=guiClass.ActiveDocument.Fusion001.LineColor
    guiClass.ActiveDocument.ActiveObject.PointColor=guiClass.ActiveDocument.Fusion001.PointColor
    appClass.ActiveDocument.recompute()

    activeDoc.removeObject("Fusion001")
    activeDoc.recompute()
    activeDoc.removeObject("Clone001")
    activeDoc.removeObject("Fusion")
    activeDoc.recompute()
    activeDoc.getObject("Body").removeObjectsFromDocument()
    activeDoc.removeObject("Body")
    activeDoc.removeObject("Clone")
    activeDoc.recompute()
    
def cuarto(appClass, guiClass, draftClass, partClass, sketcherClass, width, length, height):
    activeDoc = appClass.ActiveDocument
    activeDoc.addObject('PartDesign::Body','Body')

    activeDoc.Body.newObject('Sketcher::SketchObject','Sketch')
    activeDoc.Sketch.Support = (appClass.activeDocument().XY_Plane, [''])
    activeDoc.Sketch.MapMode = 'FlatFace'
    #appClass.ActiveDocument.recompute()
    
    sketchPolygon(appClass,partClass,sketcherClass,"Sketch",0,(-width/2,-length/2),(width/2,-length/2),
                  (width/2,length/2),(-width/2,length/2))

    padFromSketch(appClass,activeDoc.Body,activeDoc.Sketch,"Pad",height,reversePad=False)
    
    activeDoc.Body.newObject('Sketcher::SketchObject','SketchCut')
    activeDoc.SketchCut.Support = (appClass.activeDocument().XY_Plane, [''])
    activeDoc.SketchCut.MapMode = 'FlatFace'
    #appClass.ActiveDocument.recompute()
    
    sketchPolygon(appClass,partClass,sketcherClass,"SketchCut",0,(-width/2,-length/2+5),(-width/2,length/2-5),
                  (-width/2+2.5,length/2-5),(-width/2+2.5,-length/2+5))
    sketchPolygon(appClass,partClass,sketcherClass,"SketchCut",4,(-width/2+5,length/2),(width/2-5,length/2),
                  (width/2-5,length/2-2.5),(-width/2+5,length/2-2.5))
    sketchPolygon(appClass,partClass,sketcherClass,"SketchCut",8,(width/2,-length/2+5),(width/2,length/2-5),
                  (width/2-2.5,length/2-5),(width/2-2.5,-length/2+5))
    sketchPolygon(appClass,partClass,sketcherClass,"SketchCut",12,(-width/2+5,-length/2),(width/2-5,-length/2),
                  (width/2-5,-length/2+2.5),(-width/2+5,-length/2+2.5))
    
    sketchPolygon(appClass,partClass,sketcherClass,"SketchCut",16,(-width/2+7.5,-length/2+7.5),(width/2-7.5,-length/2+7.5),
                  (width/2-7.5,length/2-7.5),(-width/2+7.5,length/2-7.5))
    
    pocketFromSketch(appClass,appClass.activeDocument().Body,appClass.activeDocument().SketchCut,"Pocket",height-5,reversePocket=True)
    guiClass.activeDocument().hide("Pad")
    guiClass.activeDocument().hide("Sketch")
    guiClass.activeDocument().hide("SketchCut")
    
    activeDoc.addObject('Part::Feature','Body').Shape=appClass.ActiveDocument.Body.Shape.removeSplitter()
    activeDoc.ActiveObject.Label=appClass.ActiveDocument.Body.Label
    guiClass.ActiveDocument.Body.hide()
    guiClass.ActiveDocument.ActiveObject.ShapeColor=guiClass.ActiveDocument.Body.ShapeColor
    guiClass.ActiveDocument.ActiveObject.LineColor=guiClass.ActiveDocument.Body.LineColor
    guiClass.ActiveDocument.ActiveObject.PointColor=guiClass.ActiveDocument.Body.PointColor
    #appClass.ActiveDocument.recompute()
    activeDoc.getObject("Body").removeObjectsFromDocument()
    activeDoc.removeObject("Body")
    activeDoc.recompute()