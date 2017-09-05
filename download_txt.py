# -*- coding: utf-8 -*-

import requests
from tqdm import *

from initialize import JsonFile
from downloader import Downloader, Novel
from opencc import OpenCC
from content_fix import Content


class Downloader(Downloader):

    def get_web_page(self):
        response = requests.get(self.url)
        response.encoding = 'gb18030'

        return response.text

class SimpleToTW(Content):

    def check(self):
        file = open(self.before_update, "r", encoding="utf-8")

        opencc = OpenCC('s2tw')
        for item in tqdm(file.readlines()):
            self.content += opencc.convert(item).encode('utf-8')

        file.close()


class ContertNovel(Novel):
    def save(self):
        self.set_title(OpenCC('s2tw').convert(self.info.get_title()))

        with open(self.save_name_and_address(), mode="w", encoding="utf-8") as file:
            file.write(Downloader().get_web_page())

    def set_title(self, title=''):
        self.info.set_title(title)


def main():
    ContertNovel().save()
    SimpleToTW().update()

if __name__ == '__main__':
    main()
