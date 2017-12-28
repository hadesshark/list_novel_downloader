# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import os

import json

from JsonInit import JsonFile as JsonFile


class Book(object):

    def __del__(self):
        pass


class Bookstore(object):

    def can_not_find(self, book):
        return True if book.title not in self.book_list_title() else False

    def add_book(self, book):
        pass

    def __del__(self):
        pass


# 本身不用處理特殊 book
def bookstore_new():
    book = Book()
    bookstore = Bookstore()
    if bookstore.not_have_book(book):
        bookstore.add_book(book)


# 會有特殊 book 問題
def bookstore_update():
    bookstore = Bookstore()
    bookstore.no_finish_book_update()


def main():
    # bookstore_new()
    # bookstore_update()

    pass


if __name__ == '__main__':
    main()
