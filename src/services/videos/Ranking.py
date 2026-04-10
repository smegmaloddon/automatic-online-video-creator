# imports
from pathlib import Path
import uuid
import time

# user imports
from src.utils import temporary, terminal, configuration, directory
from src.services.videos import FFMPEG, Filter

# constants
STARTING_HEIGHT_DEPTH : int = 50

# functions
def __Numbers(
    videos : list
) -> None:
    
    font : str = temporary.content['video'].get(
        'font-family', 'C\\:/Windows/Fonts/arial.ttf'
    )

    # set colors
    colors : list[str] = [

        '#FFD700', '#C0C0C0', '#CD7F32'
    ]

    array : list = []
    for number in range(
        len(
            videos
        )
    ):
        
        # fetch color
        color : str = colors[number] if number <len(colors) else '#FFFFFF'
        
        # increase number & append
        number = number +1

        # add
        array.append(
            f"drawtext=fontfile='{font}':text='{number}':x=30:y={STARTING_HEIGHT_DEPTH *number}:fontsize=40:fontcolor={color}:borderw=4:bordercolor=black"
        )

    # create output
    output : Path = configuration.TEMPORARY /f'{uuid.uuid4()}.mp4'
    
    # build numbers process
    process: list = [
        configuration.FFMPEG,
        '-i', str(configuration.TEMPORARY /'video.mp4'),
        '-y',
        '-vf', ','.join(array),
        str(
            output
        )
    ]

    # execute
    FFMPEG.Process(
        process=process
    )

    # waitout
    time.sleep(
        1
    )

    # replace
    directory.Replace(
        old=configuration.TEMPORARY /'video.mp4',
        new=output
    )

def Run(
    videos : list
) -> None:
    
    # check if slideshows appear in videos
    if temporary.content['video'].get(
        'slideshow-enabled', False
    ) == True:
        
        # remove all slideshows
        videos = [_v for i, _v in enumerate(
            videos
        ) if i % 2 != 0]

    # add numbers first
    __Numbers(
        videos=videos
    )

    # init variables
    start : float = 0
    total : float = FFMPEG.Length(
        file=configuration.TEMPORARY /'video.mp4'
    )
    total = round(
        total, 2
    ) # round it

    array : list = []
    font : str = temporary.content['video'].get(
        'font-family', 'C\\:/Windows/Fonts/arial.ttf'
    )

    # loop through videos
    for number in range(
        len(
            videos
        )
    ):
        
        # fetch video
        video = videos[number]

        # set colors
        colors : list[str] = [

            '#FFD700', '#C0C0C0', '#CD7F32'
        ]
        color : str = colors[number] if number <len(colors) else '#FFFFFF'

        # increase number
        number = number +1

        # get length
        length : float = FFMPEG.Length(
            file=video
        )

        # fetch text
        text : str = f'this is placeholder {number}'

        # add to array, the new filter string
        array.append(
            f"drawtext=fontfile='{font}':"
            f"text='{text}':"
            f"x=80:y={STARTING_HEIGHT_DEPTH * number}:"
            f"fontsize=36:"
            f"fontcolor={color}:"
            f"borderw=3:bordercolor=black:"
            f"enable=between(t,{start},{total})"
        )

        # generate new start
        start = start +length 
        if temporary.content['video'].get(
            'slideshow-enabled', False
        ) == True:
            
            # if slideshow, add slideshow time aswell
            start = start +0.5

        start = round(
            start, 2
        )

    # build output
    output : Path = configuration.TEMPORARY /f'{uuid.uuid4()}.mp4'

    # make sure filters are correct
    filters = []
    for filter in array:

        # process
        filters.append(
            filter.strip().rstrip(',')
        )

    # build complex
    complex = "[0:v]" + ",".join(filters) + "[v]"
    print(complex)

    # build process
    process: list = [
        configuration.FFMPEG,
        '-i', str(configuration.TEMPORARY /'video.mp4'),
        '-y',
        '-filter_complex', complex,
        '-map', '[v]',
        '-map', '0:a?',
        str(output)
    ]

    # run
    FFMPEG.Process(
        process=process
    )

    # replace files
    directory.Replace(
        old=configuration.TEMPORARY /'video.mp4',
        new=output
    )