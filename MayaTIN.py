##
##
## ===========================================================================
## MIT License
## Copyright (c) 2024 
## ===========================================================================
##
## A simple tool to automate the reduction of tiles to TINs using tiles exported from TerreSculptor
## Set the fileFolder variable to your choice of location where the exported objs are. Keep in mind that the exported files will overwrite the existing ones.
## Change the reductionAmount variable to set the percentage of the reduction. The crashSafe feature is not yet implemented fully.
##
##

import maya.cmds as cmds
import os

################################
#    initialize
################################

fileFolder = "P:\\TerreScultpor\\Hungary\\Tiles\\"
#fileFolder = "P:\\TerreScultpor\\Hungary\\Tiles\\Test\\"
fileCSV = fileFolder+"\\crashSafe.csv"
tileArray = []
tileName = []
currentTile = str()
reductionAmount = 96

################################
# Whether to save the processed filenames into a CSV file in case of a crash
crashSafe = False

def saveProcessedFileName(fileName):
    with open(fileCSV, 'a') as file:
        file.write(fileName+","+"\n")
################################

def get_tiles(input):
    for path, subdirs, files in os.walk(fileFolder):
        for x in files:
            if (x.endswith(".obj") == True):
                tileArray.append(os.path.join(path, x))
                tileName.append(x)
    return tileArray

def parse_tiles():
    for currentTile in tileArray:
        newName = currentTile.replace(".obj","")
        filePath = fileFolder+currentTile
        reduce(newName, currentTile)
        if(crashSafe):
            saveProcessedFileName(filePath)
        clearScene()

#debug
def print_tiles():
    for x in tileName:
        print(x)

def reduce(newName, filePath):
    cmds.file(filePath, i=True, type="OBJ")
    selection = cmds.select(all=1)
    cmds.polyReduce(p=reductionAmount, version=1, cachingReduce=1, caching=1, keepBorder=1, replaceOriginal=1, keepBorderWeight=1)
    cmds.rename(selection, newName)
    print(filePath)
    options = "groups=0;ptgroups=0;materials={0};smoothing=1;normals={1}"
    cmds.file(filePath, exportSelected=True, type="OBJ", options=options, force=True)

def clearScene():
    cmds.file(f=True, newFile=True)

get_tiles(fileFolder)
parse_tiles()
#print_tiles()
