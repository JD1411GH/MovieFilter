
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import random
import sys
from backend import Backend

class MainGUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle("Movie filter")
        self.window.setMinimumWidth(720)
        layout = QVBoxLayout(self.window)

        # create backend instance
        self.be = Backend()

        # add filters
        filters = self.create_filters()
        layout.addWidget(filters)

        # add table
        table = self.create_table()
        table_container = QWidget()
        table_layout = QHBoxLayout(table_container)
        table_layout.addWidget(table, alignment=Qt.AlignHCenter)
        layout.addWidget(table_container)

        self.window.setLayout(layout)


    def create_filters(self):
        widget = QWidget(self.window)
        layout = QHBoxLayout(widget)

        # studio dropdown
        studios = ["All"] + self.be.get_studios()
        studio_layout = QVBoxLayout()
        studio_label = QLabel("Select Studio:")
        studio_layout.addWidget(studio_label)
        studio_dropdown = QComboBox()
        studio_dropdown.addItems(studios)
        studio_layout.addWidget(studio_dropdown)
        layout.addLayout(studio_layout)

        # category dropdown
        categories = ["All"] + self.be.get_categories()
        category_layout = QVBoxLayout()
        category_label = QLabel("Select Category:")
        category_layout.addWidget(category_label)
        category_dropdown = QComboBox()
        category_dropdown.addItems(categories)
        category_layout.addWidget(category_dropdown)
        layout.addLayout(category_layout)

        # movie rating
        movie_ratings = ["All"] + self.be.get_movie_ratings()
        movie_rating_layout = QVBoxLayout()
        movie_rating_label = QLabel("Select Movie Rating:")
        movie_rating_layout.addWidget(movie_rating_label)
        movie_rating_dropdown = QComboBox()
        movie_rating_dropdown.addItems(movie_ratings)
        movie_rating_layout.addWidget(movie_rating_dropdown)
        layout.addLayout(movie_rating_layout)

        widget.setLayout(layout)
        return widget


    def create_table(self):
        table = QTableWidget(3,4)
        table.setHorizontalHeaderLabels(["", "Title", "Actor", "Movie rating"])
        table.setMinimumWidth(600)

        table.setColumnWidth(0, 50)   # Checkbox
        table.setColumnWidth(1, 300)  # Title column
        table.setColumnWidth(2, 150)  # Actor column
        table.setColumnWidth(3, 100)  # Movie rating column

        # fetch the table entries from backend
        movies = self.be.get_movies()
        for row, movie in enumerate(movies):
            # Checkbox in column 0
            checkbox = QCheckBox()
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.addWidget(checkbox)
            cell_layout.setAlignment(checkbox, Qt.AlignCenter)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            table.setCellWidget(row, 0, cell_widget)
            
            # Title, Actor, Rating
            table.setItem(row, 1, QTableWidgetItem(movie["rel_path"]))
            table.setItem(row, 2, QTableWidgetItem(movie["actor"]))
            movie_rating_item = QTableWidgetItem(str(movie["movie_rating"]))
            movie_rating_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row, 3, movie_rating_item)

        return table


    def show(self):
        self.window.show()
        self.app.exec()

if __name__ == "__main__":
    MainGUI().show()