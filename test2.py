# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
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


class Contents(object):
    __xpath_post_num = u"//div[@class='plhin']//a//em//text()"
    __xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
    __xpath_content_list = u"//td[@class='t_f']"

    def __init__(self, url=""):
        self.obj_url = URL(url)
        self.content = ''
        self.temp_list = self.insert_list()

    def get_contents(self):
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

            self.obj_url.show_now_url()

            for item in (self.generator_item()):
                temp_list.append(item)

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



class Book(object):

    DIR_JSON_FOLDER = os.path.join("bookstore_json", title + '.json')
    DIR_TXT_FOLDER = os.path.join("bookstore_txt", title + '.txt')

    def __init__(self):
        self.content_obj = Contents(url).get_contents()

    def save_json(self):
        with open(self.DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
            json.dump(self.content_obj, f, indent=2)

    def save_txt(self):
        contents = ''
        with open(self.DIR_TXT_FOLDER, mode="w", encoding="utf-8") as txt_file:
            for item in self.content_obj:
                contents += ''.join(item["content"])
            txt_file.write(contents)


def book_setting():
    book = Book()
    book.save_json()
    book.save_txt()


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
