# -*- coding: utf-8 -*-

from . import Book
from os import path

import json

class Bookstore(object):

    def __init__(self):
        this_dir, this_filename = path.split(__file__)
        self.file_name = path.join(this_dir, "data", "Bookstore.json")
        self.book_list = []

    def get_book_list(self):
        with open(self.file_name, encoding="utf-8") as json_file:
            self.book_list = json.load(json_file)
        return self.book_list

    def book_list_title(self):
        temp_list = self.get_book_list()
        for item in temp_list:
            yield item.get('title')

    def check_have(self, book):
        return True if book.get_title() in self.book_list_title() else False

    def add_book(self, book):
        book_obj = book.get_info()
        self.book_list = self.get_book_list()
        self.book_list.append(book_obj)
        with open(self.file_name, mode="w", encoding="utf-8") as json_file:
            json.dump(self.book_list, json_file, indent=2)
