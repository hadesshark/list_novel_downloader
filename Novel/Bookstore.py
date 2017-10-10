import sqlite3
import os

from Book import Book

class Bookstore(object):

    def __init__(self):
        this_dir, this_filename = os.path.split(__file__)
        self.file_path = os.path.join(this_dir, "Data", "BookSystem.sqlite3")
        create = not os.path.exists(self.file_path)
        self.conn = sqlite3.connect(self.file_path)
        if create:
            self.create_db()

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE Bookstore ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                       "name TEXT UNIQUE NOT NULL)")
        cursor.execute("CREATE TABLE Books ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                       "title TEXT NOT NULL, "
                       "author TEXT NOT NULL, "
                       "url TEXT NOT NULL, "
                       "finish TEXT NOT NULL, "
                       "end_url TEXT NOT NULL, "
                       "end_num INTEGER NOT NULL, "
                       "Bookstore_id INTEGER NOT NULL, "
                       "FOREIGN KEY (Bookstore_id) REFERENCES Bookstore)")
        self.conn.commit()

    def add_book(self, book):
        pass

    def all_books(self):
        pass
