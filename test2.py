# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import os

import json

from JsonInit import JsonFile as JsonFile


class DownloadType(object):
    pass


class Contents(object):
    __xpath_post_num = u"//div[@class='plhin']//a//em//text()"
    __xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
    __xpath_content_list = u"//td[@class='t_f']"

    def __init__(self, update_flag=False):
        self.book_data = BookData()

        if update_flag:
            temp_url = self.book_data.get_end_url()
        else:
            temp_url = self.book_data.get_url()

        self.obj_url = URL(temp_url)
        self.content = ''
        self.temp_list = []
        self.update_flag = update_flag
        self.end_url = ''

    def get_end_url(self):  # 也不是它要做的內容
        return self.end_url

    def set_contents(self):
        DIR_JSON_FOLDER = os.path.join(
            "bookstore_json", JsonFile().__str__() + '.json')
        with open(DIR_JSON_FOLDER, encoding="utf-8") as json_file:
            contents = json.load(json_file)

        contents = self._remove_repeat_item(contents)

        self.temp_list = contents

    def _remove_repeat_item(self, contents):
        print(len(contents))

        key_list = []
        new_contents = []
        for item in contents:
            key = item.get("id")
            if key not in key_list:
                key_list.append(key)
                new_contents.append(item)

        print(len(new_contents))

        DIR_JSON_FOLDER = os.path.join(
            "bookstore_json", JsonFile().__str__() + '.json')

        with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(new_contents, f, indent=2)

        return new_contents

    # 下載
    def get_contents(self):
        if not self.update_flag:  # 初次下載
            self.temp_list = self.get_chapter_list()
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

    def get_chapter_list(self):
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


class BookData(JsonFile):
    def __init__(self):
        super().__init__()

    def get_info(self):
        return {'title': self.get_title(),
                'author': self.get_author(),
                'url': self.get_url(),
                'finish': self.get_finish(),
                'end_url': self.get_end_url()}

    def set_info(self, info):
        self.set_title(info.get('title'))
        self.set_author(info.get('author'))
        self.set_url(info.get('url'))
        self.set_finish(info.get('finish'))
        self.set_end_url(info.get('end_url'))

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

    def set_book_list(self, book_list):
        self.book_list = book_list

    def update(self):
        with open(self.file_name, mode="w", encoding="utf-8") as json_file:
            json.dump(self.book_list, json_file, indent=2)

    def book_list_title(self):
        temp_list = self.get_book_list()
        for item in temp_list:
            yield item.get('title')

    def not_have_book(self, book):
        return False if book.get_title() in self.book_list_title() else True

    def add_book(self, book):
        book.save("txt", "json")

        book_obj = book.get_info()
        self.book_list = self.get_book_list()
        self.book_list.append(book_obj)
        self.update()


class Book(BookData):

    def __init__(self, update_flag=False):
        super().__init__()

        self.book_data = BookData()  # 不該出現

        self.title = self.book_data.get_title()  # 也只有在判斷是否在書庫有使用

        self.content = Contents(update_flag)
        self.content_obj = []

        # 不行
        self.book_data.set_end_url(self.get_end_url())  # 要刪掉
        # self.book_data.update_data()

    def get_title(self):
        return self.title

    def get_end_url(self):  # 要刪掉
        return self.content.get_end_url()

    def save(self, *filetype):  # 不是它的功能
        self.content_obj = self.content.get_contents()

        if "txt" in filetype:
            self.save_txt()
        if "json" in filetype:
            self.save_json()

    def get_save_title(self):  # 不是它的功能
        return JsonFile().__str__()

    def save_json(self):  # 不是它的功能
        DIR_JSON_FOLDER = os.path.join(
            "bookstore_json", self.get_save_title() + '.json')

        with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(self.content_obj, f, indent=2)

    def save_txt(self):  # 不是它的功能
        DIR_TXT_FOLDER = os.path.join(
            "bookstore_txt", self.get_save_title() + '.txt')

        contents = ''
        with open(DIR_TXT_FOLDER, mode="w", encoding="utf-8") as txt_file:
            for item in self.content_obj:
                contents += ''.join(item["content"])
            txt_file.write(contents)


def bookstore_new():
    book = Book()
    bookstore = Bookstore()
    if bookstore.not_have_book(book):
        # book.save("txt", "json")
        bookstore.add_book(book)


def book_update(book_init_data):
    # 主要是設定 txt 和 json, 但 BookData 要先設定
    book = Book(True)
    book.save("txt", "json")

    book.set_info(book_init_data.get_info())

    return book.get_info()


def get_item(book_init_data):
    # 已完結就不再重新下載
    if book_init_data.get_finish() != "True":
        return book_update(book_init_data)
    else:
        return book_init_data.get_info()


def booklist_update(book_list):

    book_init_data = BookData()
    new_book_list = []

    for book_data in book_list:

        # 設定 Book.json
        # 每一本書都要重新設定 Book.json
        book_init_data.set_info(book_data)
        book_init_data.update_data()

        print(book_init_data.get_title() + ' 已在資料庫中')

        item = get_item(book_init_data)
        new_book_list.append(item)

        print("\n===============================================")

    return new_book_list


def bookstore_update():
    bookstore = Bookstore()
    book_list = bookstore.get_book_list()

    bookstore.set_book_list(booklist_update(book_list))
    bookstore.update()


def main():
    bookstore_new()
    # bookstore_update()


if __name__ == '__main__':
    main()
