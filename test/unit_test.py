# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.append("../")
sys.path.append("../../")

from test2 import BookData
from JsonInit import JsonFile

import json


class TestJsonInit(unittest.TestCase):
    def setUp(self):
        with open("../Book.json", encoding="utf-8") as json_file:
            self.json_data = json.load(json_file)

        self.data = JsonFile()

    def test_get_title(self):
        title_string = "\u71c3\u92fc\u4e4b\u9b42"
        self.assertEqual(self.json_data.get("title"), self.data.get_title())

    def test_get_url(self):
        url_string = "https://ck101.com/thread-3788408-1-1.html"
        self.assertEqual(self.json_data.get("url"), self.data.get_url())


if __name__ == '__main__':
    unittest.main()
