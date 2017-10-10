import sqlite3
import os


class Book(object):
    def __init__(self):
        this_dir, this_filename = os.path.split(__file__)
        self.file_path = os.path.join(this_dir, "Data", "BookSystem.sqlite3")
        create = not os.path.exists(self.file_path)
        self.conn = sqlite3.connect(self.file_path)
        if create:
            self.create_db()

        self.title = ""
        self.author = ""
        self.url = ""
        self.finish = ""

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE Books ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                       "title TEXT UNIQUE NOT NULL, "
                       "author TEXT NOT NULL, "
                       "url TEXT NOT NULL, "
                       "finish TEXT NOT NULL, "
                       "end_url TEXT NOT NULL, "
                       "end_num INTEGER NOT NULL)")
        self.conn.commit()

    def set_info(self, title, author, url, finish):

        self.title = title
        self.author = author
        self.url = url
        self.finish = finish

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO Books "
                       "(title, author, url, finish, end_url, end_num) "
                       "VALUES (?, ?, ?, ?, ?, ?)",
                       (title, author, url, finish, url, 0))

    def get_end_url(self):
        pass

    def set_end_url(self, end_url=""):
        pass

    def get_end_num(self):
        pass

    def set_end_num(self, end_num=""):
        pass

    def all_books(self):
        cursor = self.conn.cursor()
        sql = ("SELECT Books.title, Books.author, Books.url, Books.finish"
               " ORDER BY books.title")

    def all_books_title(self):
        curso = self.conn.cursor()
        sql = ("SELECT Books.id, Books.title"
                " ORDER BY Books.id")
