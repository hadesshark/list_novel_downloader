# -*- coding: utf-8 -*-


import jsoon


class Book(object):
    def __init__(self):
        with open("data/Book.json", encoding="utf-8") as json_file:
            self.json_data = json.load(json_file)

        self.title = self.json_data.get('title')
        self.url = self.json_data.get('url')
        self.author = self.json_data.get('author')
        self.finish = self.json_data.get('finish')
        self.end_url = self.json_data.get('end_url')

        self._str = ''

    def set_title(self, title=''):
        self.title = title

    def get_title(self):
        return self.title

    def set_url(self, url=''):
        self.url = url

    def get_url(self):
        return self.url

    def set_author(self, author=''):
        self.author = author

    def get_author(self):
        return self.author

    def set_finish(self, finish=''):
        self.author = author

    def get_finish(self):
        return self.finish

    def set_end_url(self, end_url=''):
        self.end_url = end_url

    def __str__(self):
        self._str = self.get_title()
        if len(self.author):
            self._str = self._str + ' 作者：{0}'.format(self.get_author())
        if self.get_finish() == "False":
            self_str = '連載中 ' + self.str

        return self._str

    def set_info(self, book):
        self.set_title(book.get('title'))
        self.set_author(book.get('author'))
        self.set_url(book.get('url'))
        self.set_finish(book.get('finish'))
        self.set_end_url(book.get('end_url'))

    def get_info(self):
        return {'title': self.get_title(),
                'author': self.get_author(),
                'url': self.get_url(),
                'finish': self.get_finish(),
                'end_url': self.get_end_url()}

    def __del__(self):
        # 忘記為何有這段判斷了
        if self.title != self.json_data.get('title'):
            with open("data/Book.json", mode="w", encoding="utf-8") as json_file:
                json.dump(self.data(), json_file, indent=2)


class Novel(Book):

    def __init__(self, url="", update_flag=False):
        super().__init__()
        self.title = self.get_title()

        # 應該是 Bookstore 有就使用更新方式，
        # 所以這部份要改
        self.content = Contents(url, update_flag)
        self.content_obj = self.content.get_contents()

        self.contents_list = []

        self.set_end_url(self.get_end_url())


def get_data():
    pass


def save(*filetype):
    if "txt" in filetype:
        save_txt()
    if "json" in filetype:
        save_json()


def save_txt():
    pass


def save_json():
    pass
