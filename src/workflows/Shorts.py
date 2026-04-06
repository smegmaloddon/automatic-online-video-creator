# imports
from pathlib import Path
import importlib

# user imports
from src.utils import temporary, configuration

# functions
def Run(
) -> None:
    
    # fetch web dictionary
    web : dict = temporary.content['web']

    # fetch type
    __type : str = web['type']

    # init dict
    dictionary : dict = {

        'user-content' : importlib.import_module('src.workflows.types.user-content')
    }

    # fetch & validate function
    func : function = dictionary[__type] or None
    if func is None:

        # raise exception
        raise Exception()
    
    # run the function
    func.Run()