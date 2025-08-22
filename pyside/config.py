import json


with open(os.path.join(ROOTDIR, 'config.json')) as f:
    self.config = json.load(f)