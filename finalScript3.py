#Composite script
#4/22/2021

import arcpy
from arcpy import env
from arcpy.sa import *
import os

arcpy.env.overwriteOutput=True

def createISO(inputPhotoFolder):
    path = inputPhotoFolder
    for file in os.listdir(path):
        if file.endswith(".tif"):
            dir_path = os.path.realpath(path)
            stringPath = dir_path.replace("\\","/")
            inputRasterPath = str(stringPath + "/" + file)
            
            print("Input: ", file)
            parts = file.split('.')
            outputRasterFile = ("".join(parts[:-1])+ '_ISO' + '.' + parts[-1])
            outputRasterPath = str(stringPath + "/" + outputRasterFile)
            Output_signature_file = ""
            print("Output: ", outputRasterPath)
            
            arcpy.gp.IsoClusterUnsupervisedClassification_sa(inputRasterPath, "2", outputRasterPath, "20", "10", Output_signature_file)
            print("\n Done. " + outputRasterFile + " has been created. \n")

def ISOtoPolygon(inputPhotoFolder):
    path = inputPhotoFolder
    for file in os.listdir(path):
        if file.endswith("ISO.tif"):
            dir_path = os.path.realpath(path)
            stringPath = dir_path.replace("\\","/")
            inputISO = str(stringPath + "/" + file)
            
            print("Input: ", inputISO)
            parts = file.split('.')
            polygonResultName = ("".join(parts[:-1])+ '_VECTOR' + '.shp')
            polygonResult = str(stringPath + "/" + polygonResultName)
            #Output_signature_file = ""
            print("Output: ",polygonResult)
            arcpy.RasterToPolygon_conversion(inputISO, polygonResult, "SIMPLIFY", "Value", "SINGLE_OUTER_PART", "")
            
            print("\n Done. " + polygonResultName + " has been created. \n")
            
def polygonToLines(inputPolygon):
    path = inputPhotoFolder
    for file in os.listdir(path):
        if file.endswith("VECTOR.shp"):

            dir_path = os.path.realpath(path)
            stringPath = dir_path.replace("\\","/")
            
            inputPolygon = str(stringPath + "/" + file)
            print("Input: ", inputPolygon) 
            parts = file.split('.')
            lineResultName = ("".join(parts[:-1])+ '_LINE' + '.shp')
            lineResult = str(stringPath + "/" + lineResultName)
            #Output_signature_file = ""
            print("Output: ",lineResult)
            arcpy.PolygonToLine_management(inputPolygon, lineResult, "IDENTIFY_NEIGHBORS")
        
            print("\n Done. " + lineResultName + " has been created. \n")


inputPhotoFolder = arcpy.GetParameterAsText(0)

arcpy.AddMessage("ISO classifying images")
iso = createISO(inputPhotoFolder)

arcpy.AddMessage("Converting classified images to polygons")
ISOtoPolygon(inputPhotoFolder)

arcpy.AddMessage("Converting polygons to lines")
polygonToLines(inputPhotoFolder)

print("success")
arcpy.AddMessage("Done.")
