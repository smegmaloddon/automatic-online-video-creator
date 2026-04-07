# imports
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, Back

# functions
def __Timestamp(
) -> str:
    
    # fetch timestamp
    timestamp : str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return timestamp

def __Type(
    text : str,
    color : str = Fore.WHITE
) -> None:
    
    # print text with color & timestamp
    print(
        f'{Fore.WHITE}{Back.BLACK}[{__Timestamp()}]{Back.RESET}: {color}{text}{Style.RESET_ALL}'
    )

def Warn(
    text : str
) -> None:
    
    # send warning
    __Type(
        text=text,
        color=Fore.YELLOW
    )

def Error(
    text : str
) -> None:
    
    # send error
    __Type(
        text=text,
        color=Fore.RED
    )

def Success(
    text : str
) -> None:
    
    # send success message
    __Type(
        text=text,
        color=Fore.GREEN
    )

def Debug(
    text : str
) -> None:
    
    # send debug message
    __Type(
        text=text,
        color=Fore.LIGHTBLUE_EX
    )