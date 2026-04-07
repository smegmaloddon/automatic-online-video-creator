# imports
from pathlib import Path

# user imports
from src.utils import configuration, temporary
from src.services.videos import FFMPEG

# functions
def Shorts(
    videos : list
) -> None:
    
    # create processed folder
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
            '-vf', 'scale=608:1080:force_original_aspect_ratio=decrease,pad=608:1080:(608-iw)/2:(1080-ih)/2:black',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            str(
                path / f'video-{number}.mp4'
            )
        ]

        FFMPEG.Process(
            process=process
        )

