# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import os

import json


class OnlineData(object):
    def __init__(self):
        with open("Book.json", encoding="utf-8") as json_file:
            self.json_data = json.load(json_file)

        self.title = self.json_data.get("title")
        self.url = self.json_data.get("url")

        temp_url = self.json_data.get("end_url")
        self.end_url = temp_url if temp_url != None else ""

        temp_num = self.json_data.get("end_num")
        self.end_num = temp_num if temp_url != None else 0

        self.flag_update = False

    def get_title(self):
        return self.title

    def get_url(self):
        return self.url

    def next_url(self):
        __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"

        temp_url = self.__analysis(__xpath_next_url)

        if temp_url != []:
            self.url = temp_url[0]
        else:
            self.url = None

    def __analysis(self, path):
        __headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) Chrome/44.0.2403.157 Safari/537.36'
        }
        try:
            response = requests.get(self.url, headers=__headers)
            return html.fromstring(response.text.encode('utf-8')).xpath(path)
        except:
            return None

    def get_end_num(self):
        return self.end_num

    def __get_chapter_num_list(self):
        __xpath_post_num = u"//div[@class='plhin']//a//em//text()"

        return self.__analysis(__xpath_post_num)

    def __get_chapter_text_list(self):
        __xpath_content_list = u"//td[@class='t_f']"
        __xpath_one_page_chapter = u".//text()"

        chapter_list = []
        for chapter in self.__analysis(__xpath_content_list):
            chapter_list.append(chapter.xpath(__xpath_one_page_chapter))
        return chapter_list

    def set_url(self, url=""):
        self.url = url

    def set_end_info(self, end_num=0):
        with open("Book.json", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        json_data["end_url"] = self.url
        json_data["end_num"] = int(end_num)

        with open("Book.json", mode="w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

    def have_chapter(self):
        if self.get_end_url() and not self.flag_update:
            self.url = self.end_url
            self.flag_update = True

        return self.url

    def get_end_url(self):
        return self.end_url

    def get_chapter_info(self):
        return list(zip(self.__get_chapter_num_list(), self.__get_chapter_text_list()))

    def save_file_dir(self):
        DIR_JSON_FOLDER = os.path.join("text", self.get_title() + '.json')

        return DIR_JSON_FOLDER

    def get_book_size(self):
        return os.path.getsize(self.save_file_dir())


class Content(object):

    def __init__(self):
        self.data = OnlineData()
        self.chapters = []

    def get_contents(self):
        __xpath_one_page_chapter = u".//text()"

        self.exists_content()

        end_num = self.data.get_end_num()

        while self.data.have_chapter():
            for index, (num, text) in enumerate(self.data.get_chapter_info()):

                if int(num) > end_num:
                    chapter = {"id": num, "text": text}
                    self.chapters.append(chapter)

                self.data.set_end_info(num)

            print(self.data.have_chapter())

            self.data.next_url()

        return self.chapters

    def exists_content(self):
        try:
            with open(self.data.save_file_dir(), encoding="utf-8") as json_file:
                self.contents = json.load(json_file)
        except:
            self.contents = []



class Book(object):

    def __init__(self):
        self.data = OnlineData()
        self.contents = Content()

    def save(self):
        DIR_JSON_FOLDER = os.path.join("text", self.data.get_title() + '.json')

        with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(self.contents.get_contents(), f, indent=2)


def new_book():
    novel = Book()
    novel.save()


def update_book():
    pass


def main():
    new_book()
    # update_book()

    # data = OnlineData()
    # print(data.get_end_num())
    # print(data.get_end_url())


if __name__ == '__main__':
    main()
