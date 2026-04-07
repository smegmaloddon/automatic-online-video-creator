# imports
from pathlib import Path
import random

# user imports
from src.utils import temporary, configuration, terminal

from src.services.web import Posts

# find Q&A posts & stitch comments together
def __Question(
) -> None:
    
    print(1)

# find & stitch user videos together
def __Videos(
) -> None:
    
    # init video requirement
    requirement : int = 8 # TODO: make dynamic with configuration & post type (studio v. short-form)
    
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

    # create folder for raw videos
    Path.mkdir(
        configuration.TEMPORARY /'raw-videos'
    )

    # loop & download videos
    for number in range(
        len(
            posts
        )
    ):
        
        # fetch post dictionary
        post : dict = posts[number]

        # fetch fallback_url
        url : str = post['media']['reddit_video']['fallback_url']

        Posts.Download(
            url=url,
            path=configuration.TEMPORARY /'raw-videos' /f'video-{number}.mp4'
        )

# functions
def Run(
) -> None:
    
    # fetch web & sub-type
    web : dict = temporary.content['web']
    __type : str = web['sub-type']

    # init dict
    dictionary : dict = {

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