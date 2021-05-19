# We are going to use the "json" library as the main method
# of configuring user-specific data.

import json

__all__ = ('load_config',)

# Sooner, when we'll have to deal with bigger requirements,
# this is going to help us a lot to ease up manipulation.
def load_config(path: str = 'dostext/data/config.json'):
    with open(path, 'r') as fp:
        return json.load(fp)
