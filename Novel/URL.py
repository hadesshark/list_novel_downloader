# -*- coding: utf-8 -*-


class URL(object):

    def __init__(self, url):
        self.url = url
        self._xpath = ""

    def set_url_xpath(self, xpath=""):
        self._xpath = xpath

    def set_url(self, url=""):
        self.url = url

    def get_url(self):
        return self.url

    def get_next_url(self):
        pass
