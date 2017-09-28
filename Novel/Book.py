# -*- coding: utf-8 -*-


class Book(object):
    def __init__(self):
        self.title = ''
        self.author = ''
        self.url = ''
        self.finish = ''

    def set_title(self, title=''):
        self.title = title

    def get_title(self):
        return self.title

    def set_author(self, author=''):
        self.author = author

    def get_author(self):
        return self.author

    def set_url(self, url=''):
        self.url = url

    def get_url(self):
        return self.url

    def set_finish(self, finish=''):
        self.finish = finish

    def get_finish(self):
        return self.finish

    def set_info(self, title='', author='', url='', finish=''):
        self.set_title(title)
        self.set_author(author)
        self.set_url(url)
        self.set_finish(finish)

    def get_info(self):
        return {'title': self.get_title(),
                'author': self.get_author(),
                'url': self.get_url(),
                'finish': self.get_finish(),
                'end_url': "",
                'end_num': 0}
