# imports
import requests
from requests import Response
import random

# user imports
from src.utils import temporary, configuration

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
def Fetch(
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
    
    url : str = f'https://www.reddit.com/r/{page}/{sort}.json?t={time}&limit=100'

    response : Response = requests.get(
        url=url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    )
    data = response.json()

    # must use this tmmr for finding videos if bool == true
    posts = data['data']['children']
    videos = [
        p['data'] for p in posts
        if p['data'].get("is_video")
    ]

    if videos:
        
        # print all
        for post in videos:

            print(post['title'])
            print(post['media']['reddit_video']['fallback_url'])