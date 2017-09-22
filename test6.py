"""
抓取一頁的簡單度，為何變成多頁就開始複雜了？

* 抓取
* 判斷
* 存取
* 書庫判斷
"""

from Novel import Bookstore, Book

from Novel import Book as novel


class Book(object):
    def __init__(self):
        self.info = novel.get_data()

    def save(self, *filetype):
        novel.save(*filetype)


def bookstore_new():
    book = Book()
    if Bookstore.check_have_book(book):
        book.save("txt", "json")
        Bookstore.add_book(book)
