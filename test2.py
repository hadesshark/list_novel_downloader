# -*- coding: utf-8 -*-
import requests
import sys
from lxml import etree, html

import json

title = "\u8d70\u9032\u4fee\u4ed9"
url = "https://ck101.com/thread-3394780-1-1.html"
author = "\u543e\u9053\u9577\u4e0d\u5b64"
finish = False


__xpath_content = u"//td[@class='t_f']//text()"
__xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"
__xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
__headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1) Chrome/44.0.2403.157 Safari/537.36'
}


def get_web_page():
    response = requests.get(url, headers=__headers)
    if response.status_code == 200:
        return etree.HTML(response.text.encode('utf-8'))
    else:
        return None


def download_analysis(path):
    return get_web_page().xpath(path)

def toString():
    response = requests.get(url, headers=__headers)
    if response.status_code == 200:
       return html.fromstring(response.text.encode('utf-8'))
    else:
        return None

# print(toString())

def down_ans(path):
    return toString().xpath(path)


__xpath_post_num = u"//div[@class='plhin']//a//em//text()"


def get_post_num():
    return download_analysis(__xpath_post_num)


def get_next_url():
    try:
        return download_analysis(__xpath_next_url)[0]
    except EOFError:
        return None


def get_all_page_num():
    all_num = download_analysis(__xpath_all_num)[0]
    print(all_num)


def chapter_list():
    return download_analysis(__xpath_content)


def chapter_list_num():
    return down_ans(u"//div[@id='postlist']")


def page_content_list():
    return down_ans(u"//td[@class='t_f']")


def save_book_json():
    temp_list = []
    for index in range(len(get_post_num())):
        chapter_num = int(get_post_num()[index])
        one_content = page_content_list()[index].text_content()
        temp_list.insert(chapter_num - 1, {"id": chapter_num, "content": one_content})

    with open(title+'.json', mode="w", encoding="utf-8") as f:
        json.dump(temp_list, f, indent=2)


def get_book_json():
    with open(title+'.json', encoding="utf-8") as json_file:
        book_json = json.load(json_file)


def json_to_txt():
    content = ""
    with open(title+ '.txt', mode="w", encoding="utf-8") as txt_file:
        for item in range(len(book_json)):
            content += book_json[item]["content"]
        txt_file.write(content)


save_book_json()
get_book_json()
json_to_txt()


def show_now_url():
    sys.stdout.write("\rurl: {0}".format(url))


def all_chapter():
    while have_url():
        show_now_url()

        chpater_list_convert_string()

        set_url(get_next_url())

    return content


def have_url():
    return True if url else False


def set_url(url):
    url = url


def chpater_list_convert_string():
    content += ''.join(chapter_list()) + '\n\n'
