##
##
## ===========================================================================
## MIT License
## Copyright (c) 2024 
## ===========================================================================
##
## A simple tool to automate the reduction of tiles to TINs using tiles exported from TerreSculptor
## Set the fileFolder variable to your choice of location where the exported objs are, making sure to leave the \\ at the end of the path too. Keep in mind that the exported files will overwrite the existing ones.
## Change the reductionAmount variable to set the percentage of the reduction. The crashSafe feature is not yet implemented fully.
##
##

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken6 import wrapInstance
from PySide6 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys

################################
#    initialize
################################

#fileFolder = "replace\\these\\paths\\with\\your\\location\\"
fileFolder = str()
fileCSV = fileFolder+"\\crashSafe.csv"
tileArray = []
tileName = []
currentTile = str()
reductionAmount = 96

################################

class tin_tool(QtWidgets.QWidget):
    window = None
    
    def __init__(self, parent = None):
        """
        Initialize class.
        """
        super(tin_tool, self).__init__(parent = parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.widgetPath = ("C:\\Users\\Imre\\Documents\\TIN_Project\\")
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath + "TIN.ui")    
        self.widget.setParent(self)
        
        self.check_lod_enable = self.widget.findChild(QtWidgets.QCheckBox, "check_lod_enable")
        self.check_lod_enable.toggled.connect(self.enable_lod)
        
        self.b_add_lod = self.widget.findChild(QtWidgets.QPushButton, "b_add_lod")
        self.b_remove_lod = self.widget.findChild(QtWidgets.QPushButton, "b_remove_lod")
        self.lod_table = self.widget.findChild(QtWidgets.QTableWidget, "lod_table")
        

    def enable_lod(self):
        check_lod_enable = self.widget.findChild(QtWidgets.QCheckBox)
        
        if (check_lod_enable.isChecked()):
            self.lod_table.setEnabled(True)
            self.b_add_lod.setEnabled(True)
            self.b_remove_lod.setEnabled(True)
        else:
            self.lod_table.setEnabled(False)
            self.b_add_lod.setEnabled(False)
            self.b_remove_lod.setEnabled(False)

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

    
def browseFolder(*args):
    fileFolder = cmds.fileDialog2(fileMode=3, okCaption="Open folder")
    return(fileFolder)

#get_tiles(fileFolder)
#parse_tiles()
#print_tiles()

def createWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'myToolWindowName' in win.objectName(): # update this name to match name below
                win.destroy()

    #QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    tin_tool.window = tin_tool(parent = mayaMainWindow)
    tin_tool.window.setObjectName('myToolWindowName') # code above uses this to ID any existing windows
    tin_tool.window.setWindowTitle("Maya TIN Optimizier")
    tin_tool.window.show()
    
createWindow()
