import json
import os
import dataset

curdir = os.path.dirname(__file__)
rootdir = os.path.dirname(curdir)

with open(os.path.join(rootdir, 'config.json')) as f:
    config = json.load(f)

def main():
    db = dataset.connect(f'sqlite:///{config["dbfile"]}')
    table = db['movies']

    select = table.find(actor_rating=6.0)
    for row in select:
        print(row['actor'])
        break


if __name__ == "__main__":
    main()