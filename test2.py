# -*- coding: utf-8 -*-
import requests
import sys
from lxml import etree, html

import json

title = "\u8d70\u9032\u4fee\u4ed9"
url = "https://ck101.com/thread-3394780-1-1.html"
author = "\u543e\u9053\u9577\u4e0d\u5b64"
finish = False


class Downloader(object):
    __xpath_post_num = u"//div[@class='plhin']//a//em//text()"
    __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"
    __xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
    __headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) Chrome/44.0.2403.157 Safari/537.36'
    }

    def __init__(self, url=""):
        self.url = url
        self.content = ''
        self.temp_list = []

    def all_chapter(self):
        while self.have_url():
            self.chpater_list_convert_string()

            self.set_url(self.get_next_url())

        return self.content

    def have_url(self):
        return True if self.url else False

    def set_url(self, url):
        self.url = url

    def toString(self):
        response = requests.get(self.url, headers=self.__headers)
        if response.status_code == 200:
            return html.fromstring(response.text.encode('utf-8'))
        else:
            return None

    def down_ans(self, path):
        return self.toString().xpath(path)

    def show_now_url(self):
        sys.stdout.write("\rurl: {0}".format(self.url))

    def get_next_url(self):
        try:
            return self.down_ans(self.__xpath_next_url)[0]
        except EOFError:
            return None

    def page_content_list(self):
        return self.down_ans(u"//td[@class='t_f']")

    def get_post_num(self):
        return self.down_ans(self.__xpath_post_num)

    def insert_list(self):
        while self.have_url():

            self.show_now_url()

            for index in range(len(self.get_post_num())):
                chapter_num = int(self.get_post_num()[index])
                one_content = self.page_content_list()[index].text_content()
                self.temp_list.insert(
                    chapter_num - 1, {"id": chapter_num, "content": one_content})

            self.set_url(self.get_next_url())

    def save_book_json(self):
        with open(title + '.json', mode="w", encoding="utf-8") as f:
            json.dump(self.temp_list, f, indent=2)

    def get_book_json(self):
        with open(title + '.json', encoding="utf-8") as json_file:
            book_json = json.load(json_file)
        return book_json

    def json_to_txt(self, book_json):
        content = ""
        with open(title + '.txt', mode="w", encoding="utf-8") as txt_file:
            for item in range(len(book_json)):
                content += book_json[item]["content"]
            txt_file.write(content)


downloader = Downloader(url)
downloader.insert_list()
downloader.save_book_json()
downloader.json_to_txt(downloader.get_book_json())
