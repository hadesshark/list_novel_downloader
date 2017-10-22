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


def get_one_page_contents(url):
    __xpath_content_list = u"//td[@class='t_f']"

    return html_string_analysis(url, __xpath_content_list)


def get_one_post_num(url):
    __xpath_post_num = u"//div[@class='plhin']//a//em//text()"

    return html_string_analysis(url, __xpath_post_num)

def get_json_contents(url):
    __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"

    __xpath_content_list = u"//td[@class='t_f']"
    __xpath_one_page_contents = u".//text()"

    json_book = []

    while url:
        one_post_num = get_one_post_num(url)
        one_page_contents = get_one_page_contents(url)

        for index, element in enumerate(one_post_num):
            chapter_num = int(element)
            one_content = one_page_contents[index].xpath(
                __xpath_one_page_contents)

            content = {"id": chapter_num, "content": one_content}
            json_book.append(content)

        temp_url = html_string_analysis(url, __xpath_next_url)

        if temp_url != []:
            url = temp_url[0]
        else:
            url = None

        print(url)

    return json_book


def load_info():
    with open("Book.json", encoding="utf-8") as json_file:
        json_data = json.load(json_file)

    title = json_data.get("title")
    author = json_data.get("author")
    url = json_data.get("url")
    finish = json_data.get("finish")

    return (title, author, url, finish)


def book_save_json(contents, title):
    DIR_JSON_FOLDER = os.path.join("text", title + '.json')

    with open(DIR_JSON_FOLDER, mode="w", encoding="utf-8") as f:
        json.dump(contents, f, indent=2)


def new_book():
    title, author, url, finish = load_info()

    book_save_json(get_json_contents(url), title)


def main():
    new_book()


if __name__ == '__main__':
    main()
