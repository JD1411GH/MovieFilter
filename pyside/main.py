
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import random
import sys
from backend import Backend

class MainGUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mainwindow = QWidget()
        self.mainwindow.setWindowTitle("Movie filter")
        self.mainwindow.setMinimumWidth(720)
        layout = QVBoxLayout(self.mainwindow)

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

        # add action buttons
        actions = self.create_actions()
        layout.addLayout(actions)

        self.mainwindow.setLayout(layout)


    def create_actions(self):
        layout = QHBoxLayout()

        # Play button
        play_button = QPushButton("Play")
        play_button.setStyleSheet("background-color: darkred; color: white;")
        layout.addWidget(play_button)

        # Edit button
        edit_button = QPushButton("Edit")
        layout.addWidget(edit_button)

        # Delete button
        delete_button = QPushButton("Delete")
        layout.addWidget(delete_button)

        # Catalog button
        catalog_button = QPushButton("Catalog")
        layout.addWidget(catalog_button)

        return layout
    
    def create_filters(self):
        widget = QWidget(self.mainwindow)
        layout = QVBoxLayout(widget)
        first_row = QHBoxLayout(widget)
        second_row = QHBoxLayout(widget)
        layout.addLayout(first_row)
        layout.addLayout(second_row)

        # studio dropdown
        studios = ["All"] + self.be.get_studios()
        studio_layout = QVBoxLayout()
        studio_label = QLabel("Select Studio:")
        studio_layout.addWidget(studio_label)
        studio_dropdown = QComboBox()
        studio_dropdown.addItems(studios)
        studio_layout.addWidget(studio_dropdown)
        first_row.addLayout(studio_layout)

        # category dropdown
        categories = ["All"] + self.be.get_categories()
        category_layout = QVBoxLayout()
        category_label = QLabel("Select Category:")
        category_layout.addWidget(category_label)
        category_dropdown = QComboBox()
        category_dropdown.addItems(categories)
        category_layout.addWidget(category_dropdown)
        first_row.addLayout(category_layout)

        # movie rating
        movie_ratings = ["All"] + self.be.get_movie_ratings()
        movie_rating_layout = QVBoxLayout()
        movie_rating_label = QLabel("Select Min Movie Rating:")
        movie_rating_layout.addWidget(movie_rating_label)
        movie_rating_dropdown = QComboBox()
        movie_rating_dropdown.addItems(movie_ratings)
        movie_rating_layout.addWidget(movie_rating_dropdown)
        first_row.addLayout(movie_rating_layout)

        # actor rating
        actor_ratings = ["All"] + self.be.get_actor_ratings()
        actor_rating_layout = QVBoxLayout()
        actor_rating_label = QLabel("Select Min Actor Rating:")
        actor_rating_layout.addWidget(actor_rating_label)
        actor_rating_dropdown = QComboBox()
        actor_rating_dropdown.addItems(actor_ratings)
        actor_rating_layout.addWidget(actor_rating_dropdown)
        first_row.addLayout(actor_rating_layout)

        # text box for Actor
        actor_layout = QVBoxLayout()
        actor_textbox = QLineEdit()
        actor_textbox.setPlaceholderText("Enter Actor Name")
        actor_layout.addWidget(actor_textbox)
        second_row.addLayout(actor_layout)

        # search button
        search_button = QPushButton("Search")
        second_row.addWidget(search_button)

        # reset button
        reset_button = QPushButton("Reset")
        # reset_button.clicked.connect(self.on_reset)
        second_row.addWidget(reset_button)

        # Go button
        go_button = QPushButton("Go")
        go_button.setStyleSheet("background-color: green; color: white;")
        second_row.addWidget(go_button)

        widget.setLayout(layout)
        return widget


    def create_table(self):
        table = QTableWidget(3,4)
        table.setHorizontalHeaderLabels(["", "Title", "Actor", "Movie rating"])
        table.setMinimumWidth(15 + 600) # row enumeration + column widths

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
        self.mainwindow.show()
        self.app.exec()

if __name__ == "__main__":
    MainGUI().show()