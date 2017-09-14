# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import os

import json


class Contents(object):
    __xpath_post_num = u"//div[@class='plhin']//a//em//text()"
    __xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
    __xpath_content_list = u"//td[@class='t_f']"

    def __init__(self, url="", update_flag=False):
        self.obj_url = URL(url)
        self.content = ''
        self.temp_list = []
        self.update_flag = update_flag
        self.end_url = ''

    def get_end_url(self):
        return self.end_url

    def set_contents(self):
        DIR_JSON_FOLDER = os.path.join(
            "bookstore_json", BookInitData().get_title() + '.json')
        with open(DIR_JSON_FOLDER, encoding="utf-8") as json_file:
            contents = json.load(json_file)
        self.temp_list = contents

    def get_contents(self):
        if not self.update_flag:
            self.temp_list = self.insert_list()
        else:
            self.temp_list = self.update()
        return self.temp_list

    def analysis(self, path):
        return self.obj_url.analysis(path)

    def page_content_list(self):
        return self.analysis(self.__xpath_content_list)

    def get_post_num(self):
        return self.analysis(self.__xpath_post_num)

    def generator_item(self):
        content_list = self.page_content_list()
        for index, element in enumerate(self.get_post_num()):
            chapter_num = int(element)
            one_content = content_list[index].xpath(u".//text()")
            yield {"id": chapter_num, "content": one_content}

    def insert_list(self):
        temp_list = []
        while self.obj_url.have_url():
            self.end_url = self.obj_url.get_url()
            self.obj_url.show_now_url()

            for item in (self.generator_item()):
                temp_list.append(item)

            self.obj_url.set_url(self.obj_url.get_next_url())
        return temp_list

    def update(self):
        self.set_contents()
        temp_list = self.temp_list
        while self.obj_url.have_url():
            self.end_url = self.obj_url.get_url()
            self.obj_url.show_now_url()

            for item in (self.generator_item()):
                if not item in temp_list:
                    sys.stdout.write("\n{0} 章更新中...".format(item['id']))
                    temp_list.append(item)
                else:
                    sys.stdout.write("\n{0} 章已有".format(item['id']))
            self.obj_url.set_url(self.obj_url.get_next_url())
        return temp_list


def html_string_analysis(url, path):
    __headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) Chrome/44.0.2403.157 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=__headers)
        return html.fromstring(response.text.encode('utf-8')).xpath(path)
    except:
        return None


class URL(object):

    __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"

    def __init__(self, url):
        self.url = url

    def have_url(self):
        return True if self.url else False

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def get_next_url(self):
        try:
            return self.analysis(self.__xpath_next_url)[0]
        except IndexError:
            return None

    def show_now_url(self):
        sys.stdout.write("\rurl: {0}".format(self.url))

    def analysis(self, path):
        return html_string_analysis(self.get_url(), path)


class BookInitData(object):
    def __init__(self):
        with open("Book.json", encoding="utf-8") as json_file:
            book = json.load(json_file)
        self.title = book.get('title')
        self.url = book.get('url')
        self.end_url = book.get('end_url')
        self.author = book.get('author')
        self.finish = book.get('finish')

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def get_end_url(self):
        return self.end_url

    def get_author(self):
        return self.author

    def get_finish(self):
        return self.finish

    def set_title(self, title):
        self.title = title

    def set_url(self, url):
        self.url = url

    def set_author(self, author):
        self.author = author

    def set_finish(self, finish):
        self.finish = finish

    def set_end_url(self, end_url):
        self.end_url = end_url

    def get_info(self):
        return {'title': self.get_title(),
                'author': self.get_author(),
                'url': self.get_url(),
                'finish': self.get_finish(),
                'end_url': self.get_end_url()}

    def set_info(self, bookstore_item):
        self.set_title(bookstore_item.get('title'))
        self.set_author(bookstore_item.get('author'))
        self.set_url(bookstore_item.get('url'))
        self.set_finish(bookstore_item.get('finish'))
        self.set_end_url(bookstore_item.get('end_url'))

    def update_data(self):
        with open("Book.json", mode="w", encoding="utf-8") as json_file:
            json.dump(self.get_info(), json_file, indent=2)


class Bookstore(object):

    def __init__(self, file_name="Bookstore.json"):
        self.book_list = ''
        self.file_name = file_name

    def get_book_list(self):
        with open(self.file_name, encoding="utf-8") as json_file:
            self.book_list = json.load(json_file)
        return self.book_list

    def update(self, book_list):
        with open(self.file_name, mode="w", encoding="utf-8") as json_file:
            json.dump(book_list, json_file, indent=2)

    def book_list_title(self):
        temp_list = self.get_book_list()
        for item in temp_list:
            yield item.get('title')

    def not_have_book(self, book):
        return False if book.get_title() in self.book_list_title() else True

    def add_book(self, book):
        book_obj = book.get_info()
        self.book_list = self.get_book_list()
        self.book_list.append(book_obj)
        self.update(self.book_list)


class Book(BookInitData):

    def __init__(self, url="", update_flag=False):
        super().__init__()
        self.title = self.get_title()

        self.content = Contents(url, update_flag)
        self.content_obj = self.content.get_contents()

        self.contents_list = []

        self.set_end_url(self.get_end_url())

    def get_end_url(self):
        return self.content.get_end_url()

    def get_contents(self):
        return self.contents_list

    def save(self, *filetype):
        if "txt" in filetype:
            self.save_txt()
        if "json" in filetype:
            self.save_json()

    def save_json(self):
        DIR_JSON_FOLDER = os.path.join("bookstore_json", self.title + '.json')

        with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(self.content_obj, f, indent=2)

    def save_txt(self):
        DIR_TXT_FOLDER = os.path.join("bookstore_txt", self.title + '.txt')

        contents = ''
        with open(DIR_TXT_FOLDER, mode="w", encoding="utf-8") as txt_file:
            for item in self.content_obj:
                contents += ''.join(item["content"])
            txt_file.write(contents)


def bookstore_new():
    book_init_data = BookInitData()
    bookstore = Bookstore()
    if bookstore.not_have_book(book_init_data):

        book = Book(book_init_data.get_url())
        book.save("txt", "json")

        bookstore.add_book(book)


def bookstore_update():
    book_init_data = BookInitData()
    bookstore = Bookstore()
    book_list = bookstore.get_book_list()

    temp_obj = []

    for obj in book_list:
        book_init_data.set_info(obj)
        book_init_data.update_data()
        print(book_init_data.get_title() + ' 已在資料庫中')

        book = Book(book_init_data.get_end_url(), True)
        book.save("txt", "json")

        book.set_info(obj)

        item = book.get_info()
        temp_obj.append(item)

        print("\n" + book_init_data.get_title() + ' 更新完畢')
        print("===============================================")
    bookstore.update(temp_obj)


def main():
    # bookstore_new()
    bookstore_update()

if __name__ == '__main__':
    main()
