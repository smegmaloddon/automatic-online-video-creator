# imports
from pathlib import Path
import random

# user imports
from src.utils import configuration, temporary, terminal, directory

# functions
def __Score(
    post : dict
) -> float:
    
    # return score
    return (
        post.get(
            'ups', 1
        ) *post.get(
            'upvote_ratio', 0.5
        )
        + post.get(
            'num_comments', 0
        ) *2
    )

def Posts(
    posts : list,
    requirement : int = 8
) -> list:
    
    # reverse order & filter down
    array : list = sorted(
        posts,
        key=lambda post: __Score(post=post),
        reverse=True
    )[:requirement]

    # return array
    return array