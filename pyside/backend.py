import openpyxl
from const import *
import json
import dataset

class Backend:
    def __init__(self):
        # read config
        with open(os.path.join(ROOTDIR, 'config.json')) as f:
            self.config = json.load(f)

        self.db = dataset.connect(self.config["dbfile"])
        self.table = self.db['movies']

        # TODO: populate all the filter values
        self.categories = []
        self.studios = []
        self.movie_ratings = []
        self.actor_ratings = []

    def catalog(self):
        self.convert_xls_to_sqlite()

    def convert_xls_to_sqlite(self):
        self.table.delete()
        workbook = openpyxl.load_workbook(filename='/home/jayanta/Downloads/LockerDB.xlsx')
        sheet = workbook.active
        headers = {header: idx for idx, header in enumerate(
            next(sheet.iter_rows(values_only=True)), 1)}
        for row in sheet.iter_rows(min_row=2, values_only=True):
            self.table.insert({
                'rel_path': row[headers['rel_path'] - 1],
                'movie_rating': row[headers['movie_rating'] - 1],
                'actor_rating': row[headers['actor_rating'] - 1],
                'actor': row[headers['actor'] - 1],
                'category': row[headers['category'] - 1],
                'studio': row[headers['studio'] - 1],
                'last_played': "",
                'playcount': row[headers['playcount'] - 1]
            })
        for row in self.table.all():
            updates = {}
            for col in ['movie_rating', 'actor_rating']:
                val = row.get(col)
                if val is not None:
                    try:
                        updates[col] = int(float(val))
                    except (ValueError, TypeError):
                        continue
            if updates:
                self.table.update(dict(id=row['id'], **updates), ['id'])

    def get_categories(self):
        # Simulate fetching categories from a database or an API
        return self.categories

    def get_movies(self   ):
        # Simulate fetching movies from a database or an API
        return [
        ]

    def get_studios(self):
        # Simulate fetching studios from a database or an API
        return self.studios

    def get_movie_ratings(self):
        # Simulate fetching movie ratings from a database or an API
        return self.movie_ratings

    def get_actor_ratings(self):
        # Simulate fetching actor ratings from a database or an API
        return self.actor_ratings