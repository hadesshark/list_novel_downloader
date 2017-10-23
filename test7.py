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

    def __get_chapter_num_list(self):
        __xpath_post_num = u"//div[@class='plhin']//a//em//text()"

        return self.__analysis(__xpath_post_num)

    def __get_chapter_text_list(self):
        __xpath_content_list = u"//td[@class='t_f']"

        return self.__analysis(__xpath_content_list)

    def set_url(self, url=""):
        self.url = url

    def get_text(self):
        return self.__get_chapter_num_list(), self.__get_chapter_text_list()

    def set_end_info(self, end_num=0):
        with open("Book.json", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        json_data["end_url"] = self.url
        json_data["end_chapter_num'"] = end_num

        with open("Book.json", mode="w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

    def have_chapter(self):
        return self.url


class Content(object):

    def __init__(self):
        self.data = OnlineData()
        self.chapters = []

    def get_contents(self):
        __xpath_one_page_chapter = u".//text()"

        while self.data.have_chapter():
            chapter_num_list, chapter_text_list = self.data.get_text()

            for index, element in enumerate(chapter_num_list):
                chapter_num = int(element)
                contents_text = chapter_text_list[index].xpath(
                    __xpath_one_page_chapter)

                chapter = {"id": chapter_num, "text": contents_text}
                self.chapters.append(chapter)

            self.data.set_end_info(chapter_num_list[-1])

            print(self.data.have_chapter())

            self.data.next_url()

        return self.chapters


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


if __name__ == '__main__':
    main()
