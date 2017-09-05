# -*- coding: utf-8 -*-
import requests
import sys
from lxml import etree

from initialize import JsonFile as JsonFile


class SettingInfo(JsonFile):
    def show_title(self):
        print(self.get_title())

    def show_title_author(self):
        print(self.__str__())


class Downloader(object):
    __xpath_content = u"//td[@class='t_f']//text()"
    __xpath_next_url = u"//div[@class='pg']/a[@class='nxt']/@href"
    __xpath_all_num = u"//div[@class='pg']/a[@class='last']//text()"
    __headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1) Chrome/44.0.2403.157 Safari/537.36'
    }

    def __init__(self, url=SettingInfo().get_url()):
        self.url = url
        self.content = ''

    def get_web_page(self):
        response = requests.get(self.url, headers=self.__headers)
        if response.status_code == 200:
            return etree.HTML(response.text.encode('utf-8'))
        else:
            return None

    def download_analysis(self, path):
        return self.get_web_page().xpath(path)

    def get_next_url(self):
        try:
            return self.download_analysis(self.__xpath_next_url)[0]
        except EOFError:
            return None

    def get_all_page_num(self):
        all_num = self.download_analysis(self.__xpath_all_num)[0]
        print(all_num)

    def chapter_list(self):
        return self.download_analysis(self.__xpath_content)

    def show_now_url(self):
        sys.stdout.write("\rurl: {0}".format(self.url))

    def all_chapter(self):
        while self.have_url():
            self.show_now_url()

            self.chpater_list_convert_string()

            self.set_url(self.get_next_url())

        return self.content

    def have_url(self):
        return True if self.url else False

    def set_url(self, url):
        self.url = url

    def chpater_list_convert_string(self):
        self.content += ''.join(self.chapter_list()) + '\n\n'


class Content(object):

    def collect(self, jsonfile=SettingInfo()):
        return Downloader(jsonfile.get_url()).all_chapter()


class Novel(object):
    file_address = r"./txt_file//"

    def __init__(self, base_setting=SettingInfo()):
        self.info = base_setting
        self.title = self.info.get_title()
        self.author = self.info.get_author()
        self.content = Content().collect(self.info)

    def save(self):
        with open(self.save_name_and_address(), 'w', encoding='utf-8') as f:
            f.write(self.content)

    # def show_title(self):
    #     self.info.show_title()

    def show_title_author(self):
        self.info.show_title_author()

    def save_name_and_address(self):
        return self.file_address + self.info.__str__()


def main():
    """
    novel save -> chapter(string) collect -> from downloader(list) get page
    """
    novel = Novel()
    novel.show_title_author()
    novel.save()


if __name__ == '__main__':
    main()
