import json
import os

CURDIR = os.path.dirname(__file__)
ROOTDIR = os.path.dirname(CURDIR)

# read config
with open(os.path.join(ROOTDIR, 'config.json')) as f:
    CONFIG = json.load(f)