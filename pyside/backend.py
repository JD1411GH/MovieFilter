class Backend:
    def __init__(self):
        # TODO: populate all the filter values
        self.categories = ["Action", "Drama", "Sci-Fi"]
        self.studios = ["Warner Bros.", "Universal Pictures", "20th Century Studios"]
        self.movie_ratings = ["5", "4", "3"]
        self.actor_ratings = ["5", "4", "3"]

    def get_categories(self):
        # Simulate fetching categories from a database or an API
        return self.categories

    def get_movies(self   ):
        # Simulate fetching movies from a database or an API
        return [
            {"rel_path": "Inception", "actor": "Leonardo DiCaprio", "movie_rating": 8.8},
            {"rel_path": "The Matrix", "actor": "Keanu Reeves", "movie_rating": 8.7},
            {"rel_path": "Interstellar", "actor": "Matthew McConaughey", "movie_rating": 8.6},
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