import os
from pathManagement import *

def rename(iPath:str, fName:str) -> bool:
    if not os.path.exists(iPath):
        return False
    parent, iName = toParentName(iPath)
    if iName == fName:
        return True
    os.rename(iPath, str(toValidUniqueName(parent, fName)))
    return True

def move():

def copy():
    