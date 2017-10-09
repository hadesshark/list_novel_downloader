# -*- coding: utf-8 -*-


class Book(object):
    def __init__(self):
        self.title = ""
        self.author = ""
        self.url = ""
        self.finish = ""
        self.end_url = ""
        self.end_num = 0

        self.content = None

    def set_title(self, title=""):
        self.title = title

    def get_title(self):
        return self.title

    def set_author(self, author=""):
        self.author = author

    def get_author(self):
        return self.author

    def set_url(self, url=""):
        self.url = url

    def get_url(self):
        return self.url

    def set_finish(self, finish=""):
        self.finish = finish

    def get_finish(self):
        return self.finish

    def set_info(self, title="", author="", url="", finish=""):
        self.set_title(title)
        self.set_author(author)
        self.set_url(url)
        self.set_finish(finish)

    def set_end_url(self, end_url=""):
        self.end_url = end_url

    def get_end_url(self):
        return self.end_url

    def set_end_num(self, end_num=0):
        pass

    def get_end_num(self):
        return self.end_num

    def get_info(self):
        return {'title': self.get_title(),
                'author': self.get_author(),
                'url': self.get_url(),
                'finish': self.get_finish(),
                'end_url': self.get_end_url(),
                'end_num': self.get_end_num()}

    def update(self, book):
        self.set_info(book.get('title'),
                      book.get('author'),
                      book.get('url'),
                      book.get('finish'))
        self.set_end_url(book.get('end_url'))
        self.set_end_num(book.get('end_num'))
