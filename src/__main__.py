# imports
from pathlib import Path

# user imports
from src.workflows import Shorts, Studio
from src.utils import JSON, temporary, configuration, directory

# functions
def __Temporary(
    identity : str
) -> None:
    
    # alter keyword
    temporary.keyword = identity
    
    # create path
    path : Path = configuration.DATA /'configuration.json'

    # fetch content
    dictionary : dict = JSON.Read(
        path=path
    )

    # fetch content
    content : dict = dictionary[temporary.keyword]

    # alter content
    temporary.content = content

def Run(
) -> None:
    
    # delete temporary childrne
    directory.Wipe(
        folder=configuration.TEMPORARY
    )
    
    # init identity
    identity : str = 'placeholder-channel'

    # fetch & alter temporary.py variables
    __Temporary(
        identity=identity
    )

    # run shorts --placeholder
    Shorts.Run()

# entry
if __name__ == '__main__':

    Run()