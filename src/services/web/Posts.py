# imports
import requests
from requests import Response
from pathlib import Path
import random

# user imports
from src.utils import temporary, configuration, terminal

# constants
SORT_PARAMETERS : list = [
    'hot',
    'new',
    'top',
    'rising'
]
TIME_PARAMETERS : list = [
    'hour',
    'day',
    'week',
    'month',
    'year',
    'all'
]

# functions
def __Video(
    child : dict
) -> bool:
    
    # init boolean
    boolean : bool = False

    # check if post is video
    if child['data'].get(
        'is_video'
    ):

        boolean = True
    
    return boolean

def __Run(
    page : str,
    video : bool = False
) -> list:
    
    # fetch random sort & time parameters
    time : str = random.choice(
        seq=TIME_PARAMETERS
    )
    sort : str = random.choice(
        seq=SORT_PARAMETERS
    )
    
    # build url
    url : str = f'https://www.reddit.com/r/{page}/{sort}.json?t={time}&limit=100'

    # send request & fetch response
    response : Response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )
    data = response.json() or None

    # catch error when fetching data
    if not data:

        raise Exception()

    # fetch posts
    posts = data['data']['children']

    # return posts if not video
    if not video:

        # return all non-video posts
        placeholder : list = [
            post['data'] for post in posts if not __Video(
                child=post
            )
        ]
        return placeholder
    
    placeholder : list = [
        post['data'] for post in posts if __Video(
            child=post
        )
    ]
    return placeholder

def Fetch(
    page : str,
    video : bool = False,
    requirement : int = 8
) -> list:
    
    # if not video required, fetch posts
    if not video:

        # return posts function
        return __Run(
            page=page
        )
    
    # init flag & content
    flag : bool = True
    content : list = []
    previous : list = []

    # loop
    while flag:

        # fetch posts
        posts : list = __Run(
            page=page,
            video=video
        )

        # add posts to content
        for post in posts:

            # if post not in previous, add to content
            if post['id'] not in previous:

                # add post & post id to respective lists
                content.append(
                    post
                )
                previous.append(
                    post['id']
                )

        # check if enough content fetched
        if len(content) >=requirement:

            flag = False
            break

    # return within the requirement
    return content[:requirement]

def Download(
    url : str,
    path : Path
) -> None:
    
    # fetch response
    response : Response = requests.get(
        url=url
    )

    try:

        # open fresh .mp4 file
        with open(
            file=path,
            mode='wb'
            # encoding='utf-8'
        ) as file:
            
            # write content to file
            file.write(
                response.content
            )
            file.close()
    
    # exception
    except Exception as error:

        raise Exception(
            error
        )

    terminal.Success(
        text='VIDEO-DOWNLOADED'
    )

def Save(
    posts : list
) -> None:
    
    return