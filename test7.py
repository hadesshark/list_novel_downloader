# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import os

import json


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


def get_next_url(url):
    __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"

    temp_url = html_string_analysis(url, __xpath_next_url)

    if temp_url != []:
        url = temp_url[0]
    else:
        url = None

    print(url)

    return url


class Contents(object):
    def __init__(self, url=""):
        self.url = url

        self.all_chapter = []

    def get_contents(self):
        __xpath_content_list = u"//td[@class='t_f']"
        __xpath_one_page_chapter = u".//text()"

        while self.url:
            chapter_num_list = self.get_chapter_num_list()
            one_page_chapter = self.get_one_page_chapter()

            for index, element in enumerate(chapter_num_list):
                chapter_num = int(element)
                content_text = one_page_chapter[index].xpath(
                    __xpath_one_page_chapter)

                chapter = {"id": chapter_num, "text": content_text}
                self.all_chapter.append(chapter)

            self.url = get_next_url(self.url)

        return self.all_chapter

    def get_chapter_num_list(self):
        __xpath_post_num = u"//div[@class='plhin']//a//em//text()"

        return html_string_analysis(self.url, __xpath_post_num)

    def get_one_page_chapter(self):
        __xpath_content_list = u"//td[@class='t_f']"

        return html_string_analysis(self.url, __xpath_content_list)


class JsonBook(object):

    def __init__(self):
        with open("Book.json", encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        self.title = json_data.get("title")
        self.author = json_data.get("author")
        self.url = json_data.get("url")
        self.finish = json_data.get("finish")

        self.contents = Contents(self.url)

    def save(self):
        DIR_JSON_FOLDER = os.path.join("text", self.title + '.json')

        with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(self.contents.get_contents(), f, indent=2)


def new_book():
    jsonbook = JsonBook()
    jsonbook.save()


def main():
    new_book()


if __name__ == '__main__':
    main()
