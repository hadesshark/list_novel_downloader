# -*- coding: utf-8 -*-
import json


class JsonFile(object):
    def __init__(self):
        with open("Book.json", encoding="utf-8") as json_file:
            self.json_data = json.load(json_file)

        self.title = self.json_data.get('title')
        self.url = self.json_data.get('url')
        self.author = self.json_data.get('author')
        self.finish = self.json_data.get('finish')
        self.end_url = self.json_data.get('end_url')
        self.str = ''

    def get_end_url(self):
        return self.end_url

    def set_end_url(self, end_url):
        self.end_url = end_url

    def get_title(self):
        return self.title

    def set_title(self, title=''):
        self.title = title

    def get_url(self):
        return self.url

    def set_url(self, url=''):
        self.url = url

    def get_author(self):
        return self.author

    def set_author(self, author=''):
        self.author = author

    def get_finish(self, finish=''):
        return self.finish

    def set_finish(self, finish='yes'):
        self.finish = finish

    def __str__(self):
        self.str = self.get_title()
        if len(self.author):
            self.str = self.str + ' 作者：{0}'.format(self.get_author())
        if self.get_finish() == False:
            self.str = '連載中 ' + self.str
        return self.str

    def data(self):
        return {
        'title': self.title,
        'url': self.url,
        'author': self.author,
        'finish': self.finish,
        'end_url': self.end_url}

    def __del__(self):
        if self.title != self.json_data.get('title'):
            with open("Book.json", mode="w", encoding="utf-8") as json_file:
                json.dump(self.data(), json_file)
