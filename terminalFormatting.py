RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
WHITE = "\033[37m"

CLEAR = "\033[2J\033[H"

def xPrint(string:str="", properties:str="", ending:str="\n") -> None:
    print(properties + string + RESET, end=ending)

def xInput(string:str="", inputProperties:str="", outputProperties:str="") -> str:
    i = input(inputProperties + string + RESET + outputProperties)
    print(RESET, end="")
    return i
