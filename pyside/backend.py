from asyncio import sleep
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
        print(f"Number of rows in movies table: {self.table.count()}")

        # TODO: populate all the filter values
        self.categories = []
        self.studios = []
        self.movie_ratings = []
        self.actor_ratings = []

    def catalog(self):
        # self.convert_xls_to_sqlite()
        pass

    def convert_xls_to_sqlite(self):
        self.db.query('DROP TABLE IF EXISTS movies')
        self.table.delete()
        workbook = openpyxl.load_workbook(filename='/home/jayanta/Downloads/LockerDB.xlsx')
        sheet = workbook.active
        for index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            self.table.insert({
                'rel_path': row[0],
                'playcount': row[1],
                'movie_rating': row[2],
                'actor': row[4],
                'category': row[5],
                'studio': row[6]
            })
        print("Data import complete")


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