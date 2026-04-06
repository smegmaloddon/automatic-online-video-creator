# imports
from pathlib import Path

# user imports
from src.utils import temporary, configuration

from src.services.web import Posts

# find Q&A posts & stitch comments together
def __Question(
) -> None:
    
    print(1)

# find & stitch user videos together
def __Videos(
) -> None:
    
    # find & return videos
    # send list[sub-reddits] 
    Posts.Fetch(
        page='aww'
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