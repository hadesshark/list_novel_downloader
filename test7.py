# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import os

import json

from JsonInit import JsonFile as JsonFile


class BookInfo(JsonFile):

    def __init__(self):
        super().__init__()

    def get_info(self):
        return {'title': self.get_title(),
                'author': self.get_author(),
                'url': self.get_url(),
                'finish': self.get_finish(),
                'end_url': self.get_end_url()}


class Contents(object):
    __xpath_post_num = u"//div[@class='plhin']//a//em//text()"
    __xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
    __xpath_content_list = u"//td[@class='t_f']"

    __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"

    __headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) Chrome/44.0.2403.157 Safari/537.36'
    }

    def __init__(self):

        self.book_info = BookInfo()
        self.url = self.book_info.get_url()

        self.all_chapter = self.get_chapter()

    def have_page(self):
        # if self.book_info.get_finish() == "False":
        #     if self.book_info.get_end_url() != "":
        #         pass
        return True if self.url else False

    def download(self, path):
        try:
            response = requests.get(self.url, headers=self.__headers)
            return html.fromstring(response.text.encode('utf-8')).xpath(path)
        except:
            return None

    def page_content_list(self):
        return self.download(self.__xpath_content_list)

    def get_post_num(self):
        return self.download(self.__xpath_post_num)

    def page_chapters(self):
        print(len(self.page_content_list()))
        print(len(self.get_post_num()))
        page_list = self.page_content_list()
        for index, element in enumerate(self.get_post_num()):
            chapter_num = int(element)
            one_content = page_list[index].xpath(u".//text()")
            yield {"id": chapter_num, "content": one_content}

    def get_next_page(self):
        try:
            self.url =  self.download(self.__xpath_next_url)[0]
        except IndexError:
            self.url = None

    def get_chapter(self):
        chapter_list = []
        while self.have_page():  # !!

            for chapter in (self.page_chapters()):
                chapter_list.append(chapter)

            self.get_next_page()  # !!

        # !!
        self.book_info.set_end_url(self.url)

        return chapter_list

    def save_title(self):
        return BookInfo().__str__()

    def save_json(self):
        DIR_JSON_FOLDER = os.path.join(
            "bookstore_json", self.save_title() + '.json')

        with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(self.all_chapter, f, indent=2)

    def save_txt(self):
        DIR_TXT_FOLDER = os.path.join(
            "bookstore_txt", self.save_title() + '.txt')

        contents = ''
        for chapter in self.all_chapter:
            contents += ''.join(chapter["content"])

        with open(DIR_TXT_FOLDER, mode="w", encoding="utf-8") as txt_file:
            txt_file.write(contents)


class Book(object):

    def __init__(self):
        self.content = Contents()

    def get_title(self):
        return BookInfo().get_title()

    def get_info(self):
        return BookInfo().get_info()

    def save(self, *filetype):
        if "json" in filetype:
            self.content.save_json()
        if "txt" in filetype:
            self.content.save_txt()

    def __del__(self):
        with open("Book.json", mode="w", encoding="utf-8") as json_file:
            json.dump(BookInfo().get_info(), json_file, indent=2)


class Bookstore(object):

    def __init__(self):
        with open("Bookstore.json", encoding="utf-8") as json_file:
            self.book_list = json.load(json_file)

    def book_list_title(self):
        for info in self.book_list:
            yield info.get('title')

    def can_not_find(self, book):
        return True if book.get_title() not in self.book_list_title() else False

    def storage(self, book):
        book.save("json", "txt")

        self.book_list.append(book.get_info())

    def __del__(self):
        with open("Bookstore.json", mode="w", encoding="utf-8") as json_file:
            json.dump(self.book_list, json_file, indent=2)


# 本身不用處理特殊 book
def bookstore_new():
    novel = Book()
    bookstore = Bookstore()
    if bookstore.can_not_find(novel):
        bookstore.storage(novel)


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
