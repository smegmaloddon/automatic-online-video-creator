# imports
from pathlib import Path
import random
import uuid

# user imports
from src.utils import configuration, temporary, directory
from src.services.videos import FFMPEG

# functions
def Shorts(
    videos : list,
    output : str = None
) -> None:
    
    # create processed folder
    processed : Path = configuration.TEMPORARY /'processed-videos'
    if not processed.exists():

        # create after verify
        Path.mkdir(
            configuration.TEMPORARY /'processed-videos'
        )

    # init path
    path : Path = configuration.TEMPORARY /'processed-videos'

    for number, video in enumerate(
        videos, 0
    ):
        
        process : list = [
            configuration.FFMPEG,
            '-i', video,
            '-vf', 'scale=608:1080:force_original_aspect_ratio=increase,crop=608:1080',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            str(
                output if output != None else path / f'video-{number}.mp4'
            )
        ]

        FFMPEG.Process(
            process=process
        )

def Random(
    path : Path,
    length : float = 16
) -> Path:
    
    # fetch duration
    duration : float = FFMPEG.Length(
        file=path
    )

    # no requirement for random
    if duration <=length:

        return None

    # fetch start time
    start = random.uniform(
        0, max(
            0, duration -length
        )
    )

    # build output
    output : Path = configuration.TEMPORARY /f'{uuid.uuid4()}.mp4' 

    process : list = [
        configuration.FFMPEG,
        '-ss', str(start),        
        '-i', path,
        '-t', str(length),   
        '-c', 'copy',             
        str(
            output
        )
    ]

    FFMPEG.Process(
        process=process
    )

    return output

def Speed(
    path : Path,
    multiplier : float = 2.0
) -> Path:
    
    # build output
    output : Path = configuration.TEMPORARY /f'{uuid.uuid4()}.mp4'

    # build process
    process = [
        configuration.FFMPEG,
        '-i', str(
            path
        ),
        '-filter_complex', '[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]',
        '-map', '[v]',
        '-map', '[a]',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        str(
            output
        )
    ]

    FFMPEG.Process(
        process=process
    )

    return output

def Normalise(
    path : Path
) -> None:
    
    # create output
    output : Path = configuration.TEMPORARY /f'{uuid.uuid4()}.mp4'

    process: list = [
        configuration.FFMPEG,
        '-i', str(path),

        # standardise encoding (IMPORTANT for concat stability)
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',

        # force clean pixel format (prevents concat glitches)
        '-pix_fmt', 'yuv420p',

        # audio standardisation (prevents DTS issues later)
        '-c:a', 'aac',
        '-b:a', '128k',

        # force consistent timing (VERY important)
        '-r', '30',

        # overwrite safely
        '-y',

        str(
            output
        )
    ]

    # run process
    FFMPEG.Process(
        process=process
    )

    # swap files
    directory.Replace(
        old=path,
        new=output
    )

def Cut(
    path : Path,
    duration : float = 0.5,
    start : float = 0
) -> None:
    
    # create output
    output : Path = configuration.TEMPORARY /f'{uuid.uuid4()}.mp4'

    # build process
    process: list = [
        configuration.FFMPEG,
        '-ss', str(start),
        '-i', str(path),
        '-t', str(duration),

        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',

        '-c:a', 'aac',
        '-b:a', '128k',

        '-y',
        str(
            output
        )
    ]

    # run ffmpeg
    FFMPEG.Process(
        process=process
    )

    # swap files
    directory.Replace(
        old=path,
        new=output
    )