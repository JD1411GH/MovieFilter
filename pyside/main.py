import subprocess
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import random
import sys
from backend import Backend
from const import *
import os

class MainGUI:
    def __init__(self):
        # global variables
        self.filtered_movies = []
        self.selected_movie = None
        self.radio_group = QButtonGroup()
        self.radio_group.setExclusive(True)
        self.radio_group.buttonClicked.connect(self.select_movie)

        # GUI setup
        self.app = QApplication(sys.argv)
        self.mainwindow = QWidget()
        self.mainwindow.setWindowTitle("Movie filter")
        self.mainwindow.setMinimumWidth(720)
        self.mainwindow.setMinimumHeight(520)
        layout = QVBoxLayout(self.mainwindow)

        # create backend instance
        self.be = Backend()

        # add filters
        filters = self.create_filters()
        layout.addWidget(filters)

        # add table
        self.table_ui = self.create_table()
        table_container = QWidget()
        table_layout = QHBoxLayout(table_container)
        table_layout.addWidget(self.table_ui, alignment=Qt.AlignHCenter)
        layout.addWidget(table_container)

        # add action buttons
        actions = self.create_actions()
        layout.addLayout(actions)

        self.mainwindow.setLayout(layout)

        

    def create_actions(self):
        layout = QHBoxLayout()

        # Play button
        play_button = QPushButton("Play")
        play_button.setStyleSheet("background-color: #ad025f; color: white;")
        play_button.clicked.connect(self.play_movie)
        layout.addWidget(play_button)

        # Edit button
        edit_button = QPushButton("Edit")
        layout.addWidget(edit_button)

        # Delete button
        delete_button = QPushButton("Delete")
        layout.addWidget(delete_button)

        # Catalog button
        catalog_button = QPushButton("Catalog")
        catalog_button.clicked.connect(self.be.catalog)
        layout.addWidget(catalog_button)

        # History button
        history_button = QPushButton("History")
        layout.addWidget(history_button)

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

        # List button
        list_button = QPushButton("List")
        list_button.setStyleSheet("background-color: green; color: white;")
        list_button.clicked.connect(self.list_movies)
        second_row.addWidget(list_button)

        widget.setLayout(layout)
        return widget


    def create_table(self):
        table = QTableWidget(10,4)
        table.setHorizontalHeaderLabels(["", "Title", "Actor", "Movie rating"])
        table.setMinimumWidth(15 + 600) # row enumeration + column widths

        table.setColumnWidth(0, 50)   # Checkbox
        table.setColumnWidth(1, 300)  # Title column
        table.setColumnWidth(2, 150)  # Actor column
        table.setColumnWidth(3, 100)  # Movie rating column

        return table


    def list_movies(self):
        # fetch the table entries from backend
        self.filtered_movies = self.be.get_movies({})
        self.radio_group = QButtonGroup()  # Reset group for each listing
        self.radio_group.setExclusive(True)
        self.radio_group.buttonClicked.connect(self.select_movie)
        self.table_ui.clearContents()
        self.selected_movie = None  # Reset selection
        for row, movie in enumerate(self.filtered_movies):
            # Radio button in column 0
            radio = QRadioButton()
            self.radio_group.addButton(radio, row)
            cell_widget = QWidget()
            cell_layout = QHBoxLayout(cell_widget)
            cell_layout.addWidget(radio)
            cell_layout.setAlignment(radio, Qt.AlignCenter)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            self.table_ui.setCellWidget(row, 0, cell_widget)

            # Title, Actor, Rating
            title = movie["rel_path"].split("\\")[-1]
            self.table_ui.setItem(row, 1, QTableWidgetItem(title))
            self.table_ui.setItem(row, 2, QTableWidgetItem(movie["actor"]))
            movie_rating_item = QTableWidgetItem(str(movie["movie_rating"]))
            movie_rating_item.setTextAlignment(Qt.AlignCenter)
            self.table_ui.setItem(row, 3, movie_rating_item)

    def select_movie(self, button):
        selected_row = self.radio_group.id(button)
        if 0 <= selected_row < len(self.filtered_movies):
            self.selected_movie = self.filtered_movies[selected_row]
        else:
            self.selected_movie = None

    def play_movie(self):
        if len(self.filtered_movies) == 0:
            self.list_movies()
        
        if self.selected_movie is None:
            movie_to_play = self.filtered_movies[0]['rel_path']
        else:
            movie_to_play = self.selected_movie['rel_path']
        if sys.platform.startswith("linux"):
            movie_to_play = movie_to_play.replace("\\", "/")

        movie_dir = CONFIG['movie_dir']
        if sys.platform.startswith("linux"):
            movie_dir = movie_dir.replace("\\", "/")
        movie_path = os.path.join(movie_dir, movie_to_play)

        # check if player supports fullscreen flag
        fullscreen = ""
        try:
            result = subprocess.run([CONFIG['movie_player'], "--help"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True,
                                timeout=5)
            if "--fullscreen" in result.stdout:
                fullscreen = "--fullscreen"
        except Exception as e:
            fullscreen = ""

        # Play
        subprocess.Popen([CONFIG['movie_player'], fullscreen, movie_path])

    def show(self):
        self.mainwindow.show()
        self.app.exec()

if __name__ == "__main__":
    MainGUI().show()