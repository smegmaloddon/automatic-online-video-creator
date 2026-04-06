# imports
import json
from json import JSONDecodeError
from pathlib import Path

# functions
def Read(
    path : Path
) -> dict:
    
    # verify path exists
    if not path.exists():

        # raise error
        raise FileNotFoundError(
            f' > file not found : {path}'
        )
    
    # init dictionary
    placeholder : dict = {}

    # create try & except block to catch JSONDECODEERROR
    try:

        # open & read file
        with open(
            file=path,
            mode='r',
            encoding='utf-8'
        ) as file:
            
            # save content to placeholder
            placeholder = json.load(
                fp=file
            )

            # close file
            file.close()

    # catch JSONDECODEERROR
    except JSONDecodeError as error:

        # raise error
        raise JSONDecodeError(
            f' > failed to decode JSON : {path}'
        )
    
    # return dictionary
    return placeholder

def Save(
    path : Path,
    content : dict
) -> None:
    
    # verify path exists
    if not path.exists():

        # raise error
        raise FileNotFoundError(
            f' > file not found : {path}'
        )
    
    # create try & except block to catch JSONDECODEERROR
    try:

        # open & write to file
        with open(
            file=path,
            mode='w',
            encoding='utf-8'
        ) as file:
            
            # write content to file
            json.dump(
                obj=content,
                fp=file,
                indent=4
            )

            # close file
            file.close()

    # catch JSONDECODEERROR
    except JSONDecodeError as error:

        # raise error
        raise JSONDecodeError(
            f' > failed to decode JSON : {path}'
        )