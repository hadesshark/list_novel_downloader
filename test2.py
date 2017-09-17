# -*- coding: utf-8 -*-
import requests
import sys
from lxml import html
import os

from JsonInit import JsonFile as JsonFile
from JsonInit import OpenWrite as OpenWrite


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

    def get_end_url(self):  # 需要修改
        return self.end_url

    def set_contents(self):
        # 需要判斷是否有內容，如果有要先取出
        contents = OpenWrite().get_book_content()
        self.temp_list = contents

    def get_contents(self):
        if not self.update_flag:
            self.temp_list = self.insert_list()
        else:
            self.temp_list = self.update()
        return self.temp_list

    def analysis(self, path):
        # 這個寫法不好，要改
        return self.obj_url.analysis(path)

    def page_content_list(self):
        # 和上面的方法一樣要改
        return self.analysis(self.__xpath_content_list)

    def get_post_num(self):
        # 不應該在 Content 內
        return self.analysis(self.__xpath_post_num)

    def generator_item(self):
        content_list = self.page_content_list()
        for index, element in enumerate(self.get_post_num()):
            chapter_num = int(element)
            one_content = content_list[index].xpath(u".//text()")
            yield {"id": chapter_num, "content": one_content}

    def insert_list(self):
        # 要改， Content 內應該判斷要屬於 Content 相關類型
        """
        temp_list = []
        while self.have_content():
            # 這一段在這有點怪
            self.obj_url.set_end_url(self.obj_url.get_url)

            for item in (self.generator_item()):
                temp_list.append(item)

            # 這一段在這也是有點怪
            self.obj_url.set_url(self.obj_url.get_next_url())
        return temp_list
        """

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


class BookInitData(JsonFile):
    def __init__(self):
        super().__init__()

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
        OpenWrite().Book_init_update(self.get_info())


class Bookstore(object):

    def __init__(self, file_name="Bookstore.json"):
        self.book_list = ''
        self.file_name = file_name
        self.openwrite = OpenWrite()

    def get_book_list(self):
        self.openwrite.get_book_list()

    def update(self, book_list):
        self.openwrite.Bookstore_list_update(book_list)

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
        self.openwrite = OpenWrite()

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
        self.openwrite.save_book_json(self.content_obj)

    def save_txt(self):
        self.openwrite.save_book_txt(self.content_obj)


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
    bookstore_new()
    # bookstore_update()


if __name__ == '__main__':
    main()
