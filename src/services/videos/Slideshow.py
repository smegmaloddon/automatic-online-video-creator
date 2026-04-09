# imports
from pathlib import Path
import uuid

# user imports
from src.utils import configuration, temporary

from src.services.videos import Filter, FFMPEG

def Create(
) -> None:
    
    # fetch sounds
    sounds : Path = configuration.ASSETS /'sound'
    videos : Path = configuration.ASSETS /'videos'

    # init paths
    sound : Path = sounds /f"{temporary.content['video']['slideshow-sound']}"
    video : Path = videos /f"{temporary.content['video']['slideshow-video']}"

    # check paths exist
    if not sound.exists() or not video.exists():

        raise FileNotFoundError()
    
    # create shorts version of video
    output : str = configuration.TEMPORARY /f'{uuid.uuid4()}.mp4'
    Filter.Shorts(
        videos=[
            video
        ],
        output=output
    )

    # build process
    process : list = [
        configuration.FFMPEG,
        '-i', str(output),
        '-i', str(sound),
        '-c:v', 'copy',  # keep video as-is
        '-c:a', 'aac',   # re-encode audio if needed
        '-shortest',     # stop at the shorter of video/audio
        str(
            configuration.TEMPORARY /'slideshow.mp4'
        )
    ]

    # run ffmpeg
    FFMPEG.Process(
        process=process
    )

    # cut slideshow.mp4 to 0s -> 0.5s --prebuilt-args
    Filter.Cut(
        path=configuration.TEMPORARY /'slideshow.mp4'
    )