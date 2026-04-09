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
    terminal.Debug(
        text='RUNNING-FFMPEG'
    )
    
    # run ffmpeg process
    subprocess.run(
        process
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
    )

def Length(
    file : Path
) -> float:
    
    # build process
    process : list = [
        configuration.FFPROBE,
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        str(
            file
        )
    ]

    # run & fetch duration
    result : list = subprocess.run(
        process,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    duration : float = float(
        result.stdout.strip()
    )

    return duration or 0