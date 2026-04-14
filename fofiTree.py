import os
from html import escape
from typing import Iterator
#
from natsort import os_sort_keygen
#
from terminalFormatting import *
from pathManagement import *

_FILE_EXPLORER_KEY = os_sort_keygen()

def _sortFofis(path:str) -> tuple[list[os.DirEntry], int, bool]:
    #
    folders : list[os.DirEntry] = []
    files : list[os.DirEntry] = []
    #
    try:
        with os.scandir(path) as iterator:
            for i in iterator:
                if i.is_dir(follow_symlinks=False):
                    folders.append(i)
                else:
                    files.append(i)
    except Exception:
        return [], 0, False
    #
    folders.sort(key=lambda item: _FILE_EXPLORER_KEY(item.name))
    files.sort(key=lambda item: _FILE_EXPLORER_KEY(item.name))
    folderCount = len(folders)
    folders.extend(files)
    return folders, folderCount, True

def printTree(
    path:str,
    #
    pathProperties:str=BOLD + WHITE,
    folderProperties:str=BOLD + RED,
    fileProperties:str=BOLD + GREEN,
    emptyFolderProperties:str=BOLD + YELLOW,
    errorProperties:str=BOLD + YELLOW
) -> None:
    #
    def _walkTree(path:str, prefix:str) -> Iterator[str]:
        #
        fofis, folderCount, success = _sortFofis(path)
        #
        if not success:
            yield f"{pathProperties}{prefix}└── {RESET}{errorProperties}<An Error Occurred>{RESET}"
            return
        if not fofis:
            yield f"{pathProperties}{prefix}└── {RESET}{emptyFolderProperties}<Empty Folder>{RESET}"
            return
        #
        lastIndex = len(fofis) - 1
        for index, fofi in enumerate(fofis):
            isLast = (index == lastIndex)
            branch = "└── " if isLast else "├── "
            prefixOfChild = prefix + ("    " if isLast else "│   ")
            #
            if index < folderCount:
                yield pathProperties + prefix + branch + RESET + folderProperties + fofi.name + RESET
                yield from _walkTree(fofi.path, prefixOfChild)
            else:
                yield pathProperties + prefix + branch + RESET + fileProperties + fofi.name + RESET
    #
    path = toAbsolutePath(path)
    while not os.path.isdir(path):
        xPrint(f"{path} isn't a valid path.", BOLD + RED)
        path = xInput("Enter a valid path to scan: ", BOLD + RED, BOLD + GREEN)
    ##
    print(folderProperties + (os.path.basename(path) or path) + RESET)
    for line in _walkTree(path, ""):
        print(line)

def saveTree(
    pathToScan:str,
    pathToSave:str,
    #
    backgroundColour:str="rgb(0,0,0)",
    pathColour:str="rgb(255,255,255)",
    folderColour:str="rgb(255,0,0)",
    fileColour:str="rgb(0,255,0)",
    emptyFolderColour:str="rgb(255,255,0)",
    errorColour:str="rgb(255,255,0)",
) -> None:
    """
    Saves file as html.
    Overwrites by default.
    Colours are CSS values like: "rgb(255,255,255)", "#ffffff", "white".
    """
    #
    def _walkTree(path:str, prefix:str) -> Iterator[str]:
        ##
        fofis, folderCount, success = _sortFofis(path)
        ##
        if not success:
            yield f'<p><span class="path">{escape(prefix + "└── ")}</span><span class="error">&lt;An Error Occurred&gt;</span></p>'
            return
        if not fofis:
            yield f'<p><span class="path">{escape(prefix + "└── ")}</span><span class="empty">&lt;Empty Folder&gt;</span></p>'
            return
        ##
        lastIndex = len(fofis) - 1
        for index, fofi in enumerate(fofis):
            isLast = (index == lastIndex)
            branch = "└── " if isLast else "├── "
            childNnoPrefix = prefix + ("    " if isLast else "│   ")
            ###
            if index < folderCount:
                yield f'<p><span class="path">{escape(prefix + branch)}</span><span class="folder">{escape(fofi.name)}</span></p>'
                yield from _walkTree(fofi.path, childNnoPrefix)
            else:
                yield f'<p><span class="path">{escape(prefix + branch)}</span><span class="file">{escape(fofi.name)}</span></p>'
    #
    pathToScan = toAbsolutePath(pathToScan)
    while not os.path.isdir(pathToScan):
        xPrint(f"{pathToScan} isn't a valid path.", BOLD + RED)
        pathToScan = xInput("Enter a valid path to scan: ", BOLD + RED, BOLD + GREEN)
    ##
    pathToSave = toAbsolutePath(pathToSave)
    pathToSaveNnoParent = os.path.dirname(pathToSave)
    while not os.path.isdir(pathToSaveNnoParent):
        xPrint(f"{pathToSaveNnoParent} isn't a folder.", BOLD + RED)
        pathToSaveNnoParent = xInput("Enter an existing folder path: ", BOLD + RED, BOLD + GREEN)
        pathToSaveNnoParent = toAbsolutePath(pathToSaveNnoParent)
        pathToSave = os.path.join(pathToSaveNnoParent, os.path.basename(pathToSave))
    ##
    with open(pathToSave, "w", encoding="utf-8", newline="\n") as file:
        file.write("<!doctype html>\n")
        file.write("<html>\n")
        file.write("<head>\n")
        file.write('<meta charset="utf-8">\n')
        file.write("<style>\n")
        file.write(f"body{{background:{backgroundColour}}}\n")
        file.write("p{white-space:pre;font-family:monospace;margin:0;line-height:1}\n")
        file.write(f".path{{color:{pathColour}}}\n")
        file.write(f".folder{{color:{folderColour}}}\n")
        file.write(f".file{{color:{fileColour}}}\n")
        file.write(f".empty{{color:{emptyFolderColour}}}\n")
        file.write(f".error{{color:{errorColour}}}\n")
        file.write("</style>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        ##
        file.write(f'<p><span class="folder">{escape(os.path.basename(pathToScan) or pathToScan)}</span></p>\n')
        for line in _walkTree(pathToScan, ""):
            file.write(line + "\n")
        ##
        file.write("</body>\n")
        file.write("</html>\n")
