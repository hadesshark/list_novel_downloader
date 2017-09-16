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
                json.dump(self.data(), json_file, indent=2)


class OpenWrite(object):
    def __init__(self):
        self.book_save_title = JsonFile().__str__()
        self.file_name = "Bookstore.json"

    # Bookstore
    def get_book_list(self):
        with open(self.file_name, encoding="utf-8") as json_file:
            book_list = json.load(json_file)
        return book_list

    # Bookstore
    def Bookstore_list_update(self, book_list):
        with open(self.file_name, mode="w", encoding="utf-8") as json_file:
            json.dump(book_list, json_file, indent=2)

    # Book
    def save_book_json(self, content_obj):
        DIR_JSON_FOLDER = os.path.join(
            "bookstore_json", self.book_save_title + '.json')

        with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(content_obj, f, indent=2)

    # Book
    def save_book_txt(self, content_obj):
        DIR_TXT_FOLDER = os.path.join(
            "bookstore_txt", self.get_save_title() + '.txt')

        contents = ''
        with open(DIR_TXT_FOLDER, mode="w", encoding="utf-8") as txt_file:
            for item in content_obj:
                contents += ''.join(item["content"])
            txt_file.write(contents)

    # Content
    def get_book_content(self):
        DIR_JSON_FOLDER = os.path.join(
            "bookstore_json", self.book_save_title + '.json')
        with open(DIR_JSON_FOLDER, encoding="utf-8") as json_file:
            contents = json.load(json_file)
        return contents

    # BookInitData
    def Book_init_update(self, info):
        with open("Book.json", mode="w", encoding="utf-8") as json_file:
            json.dump(info, json_file, indent=2)
