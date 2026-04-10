# imports
import requests
from requests import Response
from pathlib import Path
import random
from fp.fp import FreeProxy
import time

# user imports
from src.utils import temporary, configuration, terminal, JSON

# constants
PROXY_TIMEOUT : int = 6
PROXY_LIMIT : float = 0.75
SORT_PARAMETERS : list = [
    'hot',
    'new',
    'top',
    'rising'
]
TIME_PARAMETERS : list = [
    # 'hour',
    # 'day',
    # 'week', --not-generic-enough-for-algorithm
    'month',
    'year',
    'all'
]
FETCH_DELAY : float = 0.75
IGNORE_SAVE : bool = True # for not saving ids to posts.json during debug

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

def __Proxies(
) -> dict:
    
    start : float = time.time()
    
    # test proxies
    def __Test(
        proxies : dict
    ) -> bool:
        
        response : Response = None
        try:

            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=PROXY_LIMIT
            )
        except:

            # failed
            return False

        # check status code is 200
        if response.status_code != '200':

            return False
        
        return True
    
    # loop & find working proxies
    flag : bool = True
    proxies : dict = {}
    while flag:

        # fetch random proxy
        proxy = FreeProxy(
            # no args 
        ).get()
        proxies = {
            'http': proxy,
            'https': proxy
        }

        # test if proxy works
        flag = not __Test(
            proxies=proxies
        )

        # proxy finding timeout
        calculation : float = time.time() -start
        if calculation >=PROXY_TIMEOUT:

            terminal.Warn(
                text='NO-PROXY-USED'
            )
            proxies = {}
            break

    return proxies

def __Run(
    page : str,
    video : bool = False,
    afterwards : str = None
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

    # fetch proxies
    proxies = {} # __Proxies() --fuck-proxies #time.sleep() the GOAT!

    # on non-singular search, try after
    if afterwards != None:

        url = url +f'&after={afterwards}'

    # send request & fetch response
    response : Response = requests.get(
        url=url,
        proxies=proxies,
        timeout=5,
        headers = {
            "User-Agent": "my-reddit-bot/0.1 by yourusername"
        }
    )
    
    # find rate limits
    data = None
    try:

        data = response.json() or None
    except Exception as error:

        raise Exception()

    # catch error when fetching data
    if not data:

        if response.status_code == '429':

            terminal.Error(
                text='POSSIBLE-RATE-LIMIT?'
            )
        
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
    previous : list = JSON.Read(
        path=configuration.DATA /'posts.json'
    ).get(
        temporary.keyword, []
    ) # fetch previous banned ids or default to []
    afterwards : str = None

    # loop
    while flag:

        # fetch posts
        posts : list = __Run(
            page=page,
            video=video,
            afterwards=afterwards
        )

        # add posts to content
        for post in posts:

            time.sleep(
                FETCH_DELAY
            )

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

        afterwards = posts[
            len(posts) -1
        ]['id']

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

    # try
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
    
    # check if it should save
    if IGNORE_SAVE:

        return
    
    # fetch dictionary
    dictionary : dict = JSON.Read( 
        path=configuration.DATA /'posts.json'
    )

    # check if not placeholder
    placeholder : list = dictionary.get(
        temporary.keyword, []
    )

    # alter table
    placeholder +=posts

    # add & save to dictionary
    dictionary[temporary.keyword] = placeholder

    # use json.py to save back
    JSON.Save(
        path=configuration.DATA /'posts.json',
        content=dictionary
    )