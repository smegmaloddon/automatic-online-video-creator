# imports
from pathlib import Path
import shutil

# functions
def Wipe(
    folder : Path
) -> None:
    
    # loop through directory
    for file in folder.iterdir():

        # if directory then shutil.rmtree else .unlink()
        if file.is_dir():

            shutil.rmtree(
                path=file
            )
        else:

            file.unlink()

def Replace(
    old : Path,
    new : Path
) -> None:
    
    # move & overwrite
    shutil.move(
        new, old
    )