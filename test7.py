# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import os

import json


# class Bookstore(object):
#
#     def __init__(self, titlelist=[]):
#         self.booklist = titlelist
#
#     def get_booklist(self):
#         with open(self.file_name, encoding="utf-8") as json_file:
#             self.booklist = json.load(json_file)
#         return self.booklist
#
#     def set_booklist(self, booklist):
#         self.booklist = booklist
#
#     def book_list_title(self):
#         for item in self.self.get_booklist():
#             yield item.get('title')
#
#     def not_have_book(self, book=Book()):
#         return False if book.get_title() in self.book_list_title() else True
#
#     def update(self):
#         pass
#
#
# class JsonBook(object):
#
#     def __init__(self):
#         with open("Book.json", encoding="utf-8") as json_file:
#             self.json_data = json.load(json_file)
#
#         # 會變的設定
#         self.url = self.json_data.get('url')
#         self.end_url = self.json_data.get('end_url')
#
#         # 可以透過爬蟲獲得
#         self.title = self.json_data.get('title')
#         self.author = self.json_data.get('author')
#         self.finish = self.json_data.get('finish')
#
#
#     def get_url(self):
#         return self.url
#
#     def get_title(self):
#         return self.title
#
#     def get_author(self):
#         return self.author
#
#     def get_finish(self):
#         return self.finish
#
#     def get_end_url(self):
#         return self.end_url
#
#     def info(self):
#         return {
#             'title': self.title,
#             'url': self.url,
#             'author': self.author,
#             'finish': self.finish,
#             'end_url': self.end_url}
#
#     def get_save_title(self):
#         str = self.get_title()
#         if len(self.author):
#             str = str + ' 作者：{0}'.format(self.get_author())
#         if self.get_finish() == "False":
#             str = '連載中 ' + str
#
#         return str
#
# class Content(object):
#     __xpath_post_num = u"//div[@class='plhin']//a//em//text()"
#     __xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
#     __xpath_content_list = u"//td[@class='t_f']"
#
#     def __init__(self):
#         pass
#
#
# class Book(object):
#
#     def __init__(self):
#         self.json = JsonBook()
#         self.contents = Contents()
#
#     def get_title():
#         return self.json.get_title()
#
#     def get_info(self):
#         return self.json.info()
#
#     def save(self, *filetype):
#         if "txt" in filetype:
#             self.save_txt()
#         if "json" in filetype:
#             self.save_json()
#
#     def save_json(self):
#         DIR_JSON_FOLDER = os.path.join(
#             "bookstore_json", self.json.get_save_title() + '.json')
#
#         with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
#             json.dump(self.contents, f, indent=2)
#
#     def save_txt(self):
#         pass
#
#
# def bookstore_add_book():
#     book = Book()
#     bookstore = Bookstore()
#
#     if bookstore.not_have_book(book):
#
#         book.save("txt", "json")
#
#         bookstore.add_book(book)
#
#
# def bookstore_booklist_update():
#
#     bookstore = Bookstore()
#     bookstore.update()
#
#
# def main():
#     bookstore_add_book()
#     # bookstore_booklist_update()

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

def new_book():
    with open("Book.json", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    title = json_data.get("title")
    author = json_data.get("author")
    url = json_data.get("url")
    finish = json_data.get("finish")
    end_url = json_data.get("end_url")

    __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"
    __xpath_post_num = u"//div[@class='plhin']//a//em//text()"
    __xpath_content_list = u"//td[@class='t_f']"
    __xpath_one_page_contents = u".//text()"


    json_book = []

    while url:
        one_page_contents = html_string_analysis(url, __xpath_content_list)
        one_page_post_num = html_string_analysis(url, __xpath_post_num)
        for index, element in enumerate(one_page_post_num):
            chapter_num = int(element)
            one_content = one_page_contents[index].xpath(__xpath_one_page_contents)

            content = {"id": chapter_num, "content": one_content}
            json_book.append(content)

        temp_url = html_string_analysis(url, __xpath_next_url)

        if temp_url != []:
            url = temp_url[0]
        else:
            url = None

        print(url)

    DIR_JSON_FOLDER = os.path.join("text", title + '.json')

    with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
        json.dump(json_book, f, indent=2)

def main():
    new_book()


if __name__ == '__main__':
    main()
