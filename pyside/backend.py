from asyncio import sleep
import openpyxl
from const import *
import json
import dataset
import random

class Backend:
    def __init__(self):
        self.db = dataset.connect(CONFIG["dbfile"])
        self.table_movies = self.db['movies']
        self.table_actors = self.db['actors']

        # TODO: populate all the filter values
        self.categories = []
        self.studios = []
        self.movie_ratings = []
        self.actor_ratings = []
        self.actors = []

    def catalog(self):
        # self.convert_xls_to_sqlite()
        pass

    def convert_xls_to_sqlite(self):
        self.db.query('DROP TABLE IF EXISTS movies')
        self.db.query('DROP TABLE IF EXISTS actors')
        self.table_movies.delete()
        self.table_actors.delete()
        workbook = openpyxl.load_workbook(filename='/home/jayanta/Downloads/LockerDB.xlsx')
        sheet = workbook.active
        for index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
            self.table_movies.insert({
                'rel_path': row[0],
                'playcount': row[1],
                'movie_rating': row[2],
                'actor': row[4],
                'category': row[5],
                'studio': row[6]
            })
            actor = row[4]
            if actor not in self.actors:
                self.actors.append(actor)
                self.table_actors.insert({
                    'actor': row[4],
                    'actor_rating': row[3]
                })
            print(index)
        print("Data import complete")


    def delete_movie(self, rel_path):
        movie = self.table_movies.find_one(rel_path=rel_path)
        if movie:
            self.table_movies.delete(movie['id'])
        print(f"Deleted movie with rel_path: {rel_path}")

    def get_categories(self):
        # Simulate fetching categories from a database or an API
        return self.categories

    def get_movies(self, filters):
        filtered_movies = list(self.table_movies.all())
        random.shuffle(filtered_movies)
        ret = []
        for movie in filtered_movies[:10]:
            ret.append({
            'rel_path': movie['rel_path'],
            'actor': movie['actor'],
            'movie_rating': movie['movie_rating']
            })
        return ret

    def get_studios(self):
        # Simulate fetching studios from a database or an API
        return self.studios

    def get_movie_ratings(self):
        # Simulate fetching movie ratings from a database or an API
        return self.movie_ratings

    def get_actor_ratings(self):
        # Simulate fetching actor ratings from a database or an API
        return self.actor_ratings