import json
import os
import dataset
import tkinter as tk
import openpyxl

curdir = os.path.dirname(__file__)
rootdir = os.path.dirname(curdir)

with open(os.path.join(rootdir, 'config.json')) as f:
    config = json.load(f)


def convert_xls_to_sqlite(table):
    workbook = openpyxl.load_workbook(filename='LockerDB.xlsx')
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
    for row in table.all():
        updates = {}
        for col in ['movie_rating', 'actor_rating']:
            val = row.get(col)
            if val is not None:
                try:
                    updates[col] = int(float(val))
                except (ValueError, TypeError):
                    continue
        if updates:
            table.update(dict(id=row['id'], **updates), ['id'])


def create_filter_row(root, table):
    # Main frame to hold all filters
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Studio filter
    studio_frame = tk.Frame(frame)  # Subframe for studio filter
    studio_frame.pack(side=tk.LEFT, padx=10)
    studio_label = tk.Label(studio_frame, text="Studio")
    studio_label.pack()  # Default is TOP (vertical alignment)
    studios = ["All"] + sorted({row['studio']
                                for row in table.all() if 'studio' in row and row['studio']})
    studio_var = tk.StringVar()
    studio_var.set(studios[0])
    studio_dropdown = tk.OptionMenu(studio_frame, studio_var, *studios)
    studio_dropdown.pack()

    # Category filter
    category_frame = tk.Frame(frame)  # Subframe for category filter
    category_frame.pack(side=tk.LEFT, padx=10)
    category_label = tk.Label(category_frame, text="Category")
    category_label.pack()  # Default is TOP (vertical alignment)
    categories = ["All"] + sorted({row['category']
                                   for row in table.all() if 'category' in row and row['category']})
    category_var = tk.StringVar()
    category_var.set(categories[0])
    category_dropdown = tk.OptionMenu(
        category_frame, category_var, *categories)
    category_dropdown.pack()

    # actor_rating rating filter
    actor_rating_frame = tk.Frame(frame)  # Subframe for actor_rating filter
    actor_rating_frame.pack(side=tk.LEFT, padx=10)
    actor_rating_label = tk.Label(actor_rating_frame, text="actor_rating")
    actor_rating_label.pack()  # Default is TOP (vertical alignment)
    actor_ratings = ["All"] + sorted({row['actor_rating']
                                      for row in table.all() if 'actor_rating' in row and row['actor_rating']})
    actor_rating_var = tk.StringVar()
    actor_rating_var.set(actor_ratings[0])
    actor_rating_dropdown = tk.OptionMenu(
        actor_rating_frame, actor_rating_var, *actor_ratings)
    actor_rating_dropdown.pack()

    # actor filter
    actor_frame = tk.Frame(frame)
    actor_frame.pack(side=tk.LEFT, padx=10)
    actor_label = tk.Label(actor_frame, text="actor")
    actor_label.pack()
    actors = ["All"] + sorted({row['actor']
                               for row in table.all() if 'actor' in row and row['actor']})
    actor_var = tk.StringVar()
    actor_var.set(actors[0])
    actor_dropdown = tk.OptionMenu(
        actor_frame, actor_var, *actors)
    actor_dropdown.pack()

    # movie_rating filter
    movie_rating_frame = tk.Frame(frame)
    movie_rating_frame.pack(side=tk.LEFT, padx=10)
    movie_rating_label = tk.Label(movie_rating_frame, text="movie_rating")
    movie_rating_label.pack()
    movie_ratings = ["All"] + sorted({row['movie_rating']
                                      for row in table.all() if 'movie_rating' in row and row['movie_rating']})
    movie_rating_var = tk.StringVar()
    movie_rating_var.set(movie_ratings[0])
    movie_rating_dropdown = tk.OptionMenu(
        movie_rating_frame, movie_rating_var, *movie_ratings)
    movie_rating_dropdown.pack()


def main():
    db = dataset.connect(f'sqlite:///{config["dbfile"]}')
    table = db['movies']
    table.delete()
    convert_xls_to_sqlite(table)

    root = tk.Tk()
    root.title("Movie Filter")
    create_filter_row(root, table)
    root.mainloop()

if __name__ == "__main__":
    main()
