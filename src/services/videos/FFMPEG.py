# imports
from pathlib import Path
import subprocess

# user imports
from src.utils import configuration, temporary, terminal

# functions
def Process(
    process : list
) -> None:
    
    # TODO: create progress bar
    
    # run ffmpeg process
    subprocess.run(
        process
    )