# imports
from pathlib import Path

# user imports
from src.utils import configuration, temporary

from src.services.videos import FFMPEG

# functions
def Merge(
    videos : list,
    output : Path
) -> None:
    
    # open videos.txt
    with open(
        file=configuration.TEMPORARY /'videos.txt',
        mode='w',
        encoding='utf-8'
    ) as file:
        
        # loop & format
        for video in videos:

            file.write(
                f"file '{video.as_posix()}'\n"
            )

    process: list = [
        configuration.FFMPEG,
        '-f', 'concat',
        '-safe', '0',
        '-i', str(configuration.TEMPORARY / 'videos.txt'),
        '-c:v', 'libx264',        # re-encode video
        '-preset', 'fast',         # faster encoding without losing much quality
        '-crf', '18',              # near-lossless quality
        '-c:a', 'aac',             # re-encode audio safely
        '-b:a', '192k',            # decent audio bitrate
        '-threads', '0',           # use all CPU cores
        str(output)
    ]

    FFMPEG.Process(
        process=process
    )