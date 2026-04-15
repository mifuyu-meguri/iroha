import os
import shutil
from pathlib import Path
#
from terminalFormatting import *
from pathManagement import *

_SKIP_STRING = "PASS"

def rename(iPath:str, fName:str) -> bool:
    #
    parent, iName = sepParentName(iPath)
    fPath = toValidUniqueName(parent, fName)
    _, fName = sepParentName(fName)
    if iName == fName:
        return True
    #
    while not os.path.exists(iPath):
        xPrint(f"{iPath} doesn't exist. Enter a new path to rename to: {fName}", BOLD + RED)
        xPrint(f"To skip this fofi, pass an empty string, then pass: '{_SKIP_STRING}'.", DIM)
        _iPath = xInput("New initial path: ", BOLD + RED, BOLD + GREEN)
        if not _iPath:
            confirmation = xInput("Skip fofi: ", BOLD + RED, BOLD + GREEN)
            if confirmation == _SKIP_STRING:
                return False
        iPath = _iPath
    #
    Path(iPath).rename(fPath)
    return True

def move(iPath:str, fParent:str, fName:str) -> bool:
    shutil.move()
    return True

def copy(iPath:str, fParent:str, fName:str) -> bool:
    if :
        shutil.copy2()
    else:
        shutil.copytree()
    return True
