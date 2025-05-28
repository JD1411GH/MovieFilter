import json
import os
import dataset
from openpyxl import load_workbook

curdir = os.path.dirname(__file__)
rootdir = os.path.dirname(curdir)

with open(os.path.join(rootdir, 'config.json')) as f:
    config = json.load(f)

def main():
    db = dataset.connect(f'sqlite:///{config["dbfile"]}')
    table = db['movies']

    workbook = load_workbook(filename='LockerDB.xlsx')
    sheet = workbook.active
    headers = {header: idx for idx, header in enumerate(next(sheet.iter_rows(values_only=True)), 1)}
    for row in sheet.iter_rows(min_row=2, values_only=True):
        table.insert({
            'rel_path': row[headers['rel_path'] - 1],
            'movie_rating': row[headers['movie_rating'] - 1],
            'actor_rating': row[headers['actor_rating'] - 1],
            'actor': row[headers['actor'] - 1],
            'category': row[headers['category'] - 1],
            'studio': row[headers['studio'] - 1],
            'last_played': "",
            'playcount': row[headers['playcount'] - 1]
            })


    


if __name__ == "__main__":
    main()