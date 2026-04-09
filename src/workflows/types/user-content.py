# imports
from pathlib import Path
import random
import shutil

# user imports
from src.utils import temporary, configuration, terminal, directory

from src.services.web import Posts
from src.services.videos import Filter, Merge, Slideshow

# find Q&A posts & stitch comments together
def __Question(
) -> None:
    
    print(1)

# find & stitch user videos together
def __Videos(
) -> None:
    
    # init video requirement
    requirement : int = 7 # TODO: make dynamic with configuration & post type (studio v. short-form)
    
    # find & return videos
    posts : list = Posts.Fetch(
        page=random.choice(
            seq=temporary.content['web']['sub-reddits']
        ),
        video=True,
        requirement=requirement
    )

    # if no posts found, raise exception
    if len(posts) == 0:

        # raise exception
        raise Exception()
    
    # loop & debug print titles
    text : list = []
    for post in posts:

        # fetch & build str
        id : str = post['id']

        # format
        text.append(
            id
        )

    # success print
    terminal.Success(
        text=text
    )

    # save ids for future
    Posts.Save(
        posts=text
    )

    videos : list = []

    # loop & download videos
    for number in range(
        len(
            posts
        )
    ):
        
        # fetch post dictionary
        post : dict = posts[number]

        # fetch fallback_url
        url : str = post['media']['reddit_video']['dash_url']

        videos.append(
            url
        )

    # turn videos into short formats
    Filter.Shorts(
        videos=videos
    )

    # filter to <=8s & replace old
    processed : Path = configuration.TEMPORARY /'processed-videos'
    for file in processed.iterdir():

        # filter & return path
        updated : Path = Filter.Random(
            path=file
        )

        # video did not require filter()
        if updated is None:

            continue
        
        # speed video up
        multiplied : Path = Filter.Speed(
            path=updated
        )
        updated.unlink()

        # replace old with new
        directory.Replace(
            old=file,
            new=multiplied
        )

    # check if slideshow-enabled is true
    boolean : bool = temporary.content['video'].get(
        'slideshow-enabled', False
    )
    if not boolean:

        # create videos list
        videos = [
            video for video in processed.iterdir()
        ]
    else:

        # create slideshow directory because ffmpeg is a bitch about single file being multiple use
        Path.mkdir(
            configuration.TEMPORARY /'slideshows'
        )

        # create slideshow cinematic
        Slideshow.Create()

        # init path
        path : Path = configuration.TEMPORARY /'slideshow.mp4'

        # create videos list
        videos = [] # reset videos
        number : int = 0
        for video in processed.iterdir():

            # add video & path
            videos.append(
                video
            )
            
            # create new path & copy old
            placeholder : Path = configuration.TEMPORARY /'slideshows' /f'slideshow-{number}.mp4'
            shutil.copy(
                path, placeholder
            )

            Filter.Normalise(
                path=placeholder
            )

            # add placeholder path
            videos.append(
                placeholder
            )

            # increase number
            number = number +1

    Merge.Merge(
        videos=videos,
        output=configuration.TEMPORARY /'video.mp4'
    )

# functions
def Run(
) -> None:
    
    # fetch web & sub-type
    web : dict = temporary.content['web']
    __type : str = web['sub-type']

    # init dict
    dictionary : dict = {

        # add arguments for when studio.py is involved to alternate what functions do
        # i.e Shorts vs Long-Form
        'Q&A' : __Question,
        'user-videos' : __Videos
    }

    # fetch & validate function
    func : function = dictionary[__type] or None
    if func is None:

        # raise exception
        raise Exception()

    # run the function
    func()