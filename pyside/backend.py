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
        pass
    
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