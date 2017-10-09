# from Novel.Bookstore import Bookstore
#
# bookstore = Bookstore()
# for item in bookstore.book_list_title():
#     print(item)

import sqlite3
import os


# def connect(name):
#     create = not os.path.exists(name)
#     conn = sqlite3.connect(name)
#     if create:
#         cursor = conn.cursor()
#         cursor.execute("CREATE TABLE directors ("
#                        "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
#                        "name TEXT UNIQUE NOT NULL)")
#         cursor.execute("CREATE TABLE dvds ("
#                        "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
#                        "title TEXT NOT NULL, "
#                        "year INTEGER NOT NULL, "
#                        "duration INTEGER NOT NULL, "
#                        "director_id INTEGER NOT NULL, "
#                        "FOREIGN KEY (director_id) REFERENCES directors)")
#         conn.commit()
#
#     return conn
#
#
# def add_dvd(conn, title, year, duration, director):
#     director_id = get_and_set_director(conn, director)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO dvds "
#                    "(title, year, duration, director_id) "
#                    "VALUES (?, ?, ?, ?)",
#                    (title, year, duration, director_id))
#     conn.commit()
#
#
# def get_and_set_director(conn, director):
#     director_id = get_director_id(conn, director)
#     if director_id is not None:
#         return director_id
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO directors (name) VALUES (?)",
#                    (director,))
#     conn.commit()
#     return get_director_id(conn, director)
#
#
# def get_director_id(conn, director):
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM directors WHERE name=?",
#                    (director,))
#     fields = cursor.fetchone()
#     return fields[0] if fields is not None else None
#
#
# def all_dvds(conn):
#     cursor = conn.cursor()
#     sql = ("SELECT dvds.title, dvds.year, dvds.duration, "
#            "directors.name FROM dvds, directors "
#            "WHERE dvds.director_id = directors.id"
#            " ORDER BY dvds.title")
#     cursor.execute(sql)
#     return [(str(fields[0]), fields[1], fields[2], str(fields[3]))
#             for fields in cursor]
#
#
# def all_directors(conn):
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM directors ORDER BY name")
#     return [str(fields[0]) for fields in cursor]
#
#
# db_name = 'dvd_library.sqlite3'
# conn = connect(db_name)
# add_dvd(conn, 'Python Tutorial 2013', 2013, 1, 'Justin')
# print(all_directors(conn))
# print(all_dvds(conn))

class DataBase(object):

    def __init__(self, name):
        create = not os.path.exists(name)
        self.conn = sqlite3.connect(name)
        if create:
            self.create_db()

    def create_db(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE directors ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                       "name TEXT UNIQUE NOT NULL)")
        cursor.execute("CREATE TABLE dvds ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, "
                       "title TEXT NOT NULL, "
                       "year INTEGER NOT NULL, "
                       "duration INTEGER NOT NULL, "
                       "director_id INTEGER NOT NULL, "
                       "FOREIGN KEY (director_id) REFERENCES directors)")
        self.conn.commit()

    def add_dvd(self, title, year, duration, director):
        director_id = self._get_and_set_director(director)
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO dvds "
                       "(title, year, duration, director_id) "
                       "VALUES (?, ?, ?, ?)",
                       (title, year, duration, director_id))
        self.conn.commit()

    def _get_and_set_director(self, director):
        director_id = self._get_director_id(director)
        if director_id is not None:
            return director_id
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO directors (name) VALUES (?)",
                       (director,))
        self.conn.commit()
        return self._get_director_id(director)

    def _get_director_id(self, director):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM directors WHERE name=?",
                       (director,))
        fields = cursor.fetchone()
        return fields[0] if fields is not None else None

    def all_dvds(self):
        cursor = self.conn.cursor()
        sql = ("SELECT dvds.title, dvds.year, dvds.duration, "
               "directors.name FROM dvds, directors "
               "WHERE dvds.director_id = directors.id"
               " ORDER BY dvds.title")
        cursor.execute(sql)
        return [(str(fields[0]), fields[1], fields[2], str(fields[3]))
                for fields in cursor]

    def all_directors(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM directors ORDER BY name")
        return [str(fields[0]) for fields in cursor]


db_name = 'dvd_library.sqlite3'
db = DataBase(db_name)
db.add_dvd("Python Tutorial 2013", 2013, 1, "Justin")
print(db.all_directors())
print(db.all_dvds())
