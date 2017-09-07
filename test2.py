# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import time
import os

import json

with open("Book.json", encoding="utf-8") as json_file:
    book = json.load(json_file)

title = book.get('title')
url = book.get('url')
author = book.get('author')
finish = book.get('finish')


with open("Bookstore.json", encoding="utf-8") as json_file:
    bookstore = json.load(json_file)


def book_list_item():
    for item in bookstore:
        yield item.get('title')


class Downloader(object):
    __xpath_post_num = u"//div[@class='plhin']//a//em//text()"
    __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"
    __xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
    __headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) Chrome/44.0.2403.157 Safari/537.36'
    }
    DIR_JSON_FOLDER = os.path.join("bookstore_json", title + '.json')
    DIR_TXT_FOLDER = os.path.join("bookstore_txt", title + '.txt')

    def __init__(self, url=""):
        self.url = url
        self.content = ''
        self.temp_list = []

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
        except IndexError:
            return None

    def page_content_list(self):
        return self.down_ans(u"//td[@class='t_f']")

    def get_post_num(self):
        return self.down_ans(self.__xpath_post_num)

    def generator_item(self):
        content_list = self.page_content_list()
        for index, element in enumerate(self.get_post_num()):
            chapter_num = int(element)
            one_content = content_list[index].xpath(u".//text()")
            yield {"id": chapter_num, "content": one_content}

    def insert_list(self):
        while self.have_url():

            self.show_now_url()
            tStart = time.time()

            for item in (self.generator_item()):
                self.temp_list.append(item)

            tEnd = time.time()
            tFinish = tEnd - tStart
            sys.stdout.write("\nIt cost {} sec\n".format(tFinish))
            if (tFinish < 3):
                time.sleep(3 - tFinish)

            self.set_url(self.get_next_url())

    def save_book_json(self):
        with open(self.DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(self.temp_list, f, indent=2)

    def get_book_json(self):
        with open(self.DIR_JSON_FOLDER, encoding="utf-8") as json_file:
            book_json = json.load(json_file)
        return book_json


class JsonToTxt(object):
    
    DIR_TXT_FOLDER = os.path.join("bookstore_txt", title + '.txt')
    content = ''
    
    def __init__(self, jsonfile):
        self.book_json = jsonfile
    
    def convert(self):
        with open(self.DIR_TXT_FOLDER, mode="w", encoding="utf-8") as txt_file:
            for item in self.book_json:
                self.content += ''.join(item["content"])
            txt_file.write(self.content)


def book_setting():
    downloader = Downloader(url)
    downloader.insert_list()
    downloader.save_book_json()
    JsonToTxt(downloader.get_book_json()).convert()


def main():
    if not title in book_list_item():
        
        book_setting()
        
        item = {'title': title, 'author': author, 'url': url, 'finish': finish}
        bookstore.append(item)
        with open("Bookstore.json", mode="w", encoding="utf-8") as json_file:
            json.dump(bookstore, json_file, indent=2)
    else:
        print(title + '已經有下載過了')



if __name__ == '__main__':
    main()

