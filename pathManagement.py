import os
from pathlib import Path
#
from terminalFormatting import *

_ILLEGAL_CHARACTERS = str.maketrans({
    ord("*"): "＊",
    ord(":"): "：",
    ord("|"): "｜",
    ord("?"): "？",
    ord("<"): "＜",
    ord(">"): "＞",
    ord("/"): "／",
    ord("\\"):"＼",
    ord('"'):  "”",

    0x00: None, 0x01: None, 0x02: None, 0x03: None,
    0x04: None, 0x05: None, 0x06: None, 0x07: None,
    0x08: None, 0x09: None, 0x0A: None, 0x0B: None,
    0x0C: None, 0x0D: None, 0x0E: None, 0x0F: None,
    0x10: None, 0x11: None, 0x12: None, 0x13: None,
    0x14: None, 0x15: None, 0x16: None, 0x17: None,
    0x18: None, 0x19: None, 0x1A: None, 0x1B: None,
    0x1C: None, 0x1D: None, 0x1E: None, 0x1F: None,
})

_ILLEGAL_NAMES = [
    "CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$", "CLOCK$",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM¹", "COM²", "COM³",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9", "LPT¹", "LPT²", "LPT³",
]

def length_FE(string:str) -> int:
    return len(string.encode("utf-16-le")) // 2

def sepNameExtensions(name:str) -> tuple[str, str]:
    suffixes = "".join(Path(name).suffixes)
    stem = name[:-len(suffixes)] if suffixes else name
    return stem, suffixes

def sepParentName(path:str) -> tuple[str, str]:
    """
    Prefers parent over name.
    """
    path = path.rstrip("\\")
    path = path.rsplit("\\", 1)
    if len(path) == 1:
        return path[0], "" # Prefers parent over name.
    else:
        return path[0], path[1]
    
def toAbsolutePath(path:str) -> str:
    """
    Note: pathlib.Path has no os.path.expandvars() equivalent.
    """
    if len(path) == 2 and path[0].isalpha() and path[1] == ":":
        return path[0].upper() + ":\\"
    return os.path.abspath(os.path.expandvars(path))
    
def toValidUniqueName(fofiParentPath:str, fofiName:str, unique:bool=True) -> str:
    fofiParentPath = Path(toAbsolutePath(fofiParentPath))
    while True:
        #
        fofiName = fofiName.translate(_ILLEGAL_CHARACTERS).rstrip(" .").lstrip(" ")
        #
        if not fofiName:
            fofiName = "_"
        #
        fofiPath = fofiParentPath / fofiName
        stem, suffixes = sepNameExtensions(fofiName)
        if stem.upper() in _ILLEGAL_NAMES:
            stem = "_" + stem[1:]
            fofiPath = fofiParentPath / ( stem + suffixes )
        #
        if unique:
            nextIndex = 2
            while fofiPath.exists():
                fofiPath = fofiParentPath / f"{stem} ({nextIndex}){suffixes}"
                nextIndex += 1
        #
        if length_FE(str(fofiPath)) > 259 or length_FE(fofiPath.name) > 255:
            xPrint(f"The final name is too long: {fofiPath}", BOLD + RED)
            fofiName = xInput("Enter new name (without extensions): ", BOLD + RED, BOLD + GREEN)
            _, _suffixes = sepNameExtensions(fofiName)
            fofiName = fofiName if _suffixes else (fofiName + suffixes)
            continue
        #
        return str(fofiPath)
