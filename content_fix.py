# -*- coding: utf-8 -*-
import os
import shutil

from tqdm import *

from initialize import JsonFile as JsonFile


def show_information(file_name, system_name):
    print("{0} size: {1}".format(file_name, os.path.getsize(system_name)))


class Content(object):

    def __init__(self):
        self.txt_space = r"./txt_file//"
        self.before_update = self.txt_space + "temp.txt"
        self.after_update = self.txt_space + "temp2.txt"

        self.json_file = JsonFile()
        self.finish_version = self.txt_space + self.json_file.__str__()
        self.file_name = self.json_file.__str__()

        self.content = "".encode('utf-8')

    def folder_remove(self, file_name=''):
        if os.path.isfile(file_name):
            os.remove(file_name)

    def folder_make(self, file_name=''):
        if not(os.path.exists(file_name)):
            os.mkdir(file_name)

    def txt_space_fix(self):
        self.folder_make(self.txt_space)

        self.folder_remove(self.before_update)
        self.folder_remove(self.after_update)


    def check(self):
        file = open(self.before_update, "rb")

        for item in tqdm(file.readlines()):
            if len(item) == 1:
                continue
            elif "  ".encode('utf-8') in item:  # 多空格行
                continue
            elif "本帖最後由".encode('utf-8') in item:
                continue
            # elif len(item) <= 3:
            #     continue
            else:
                self.content += item
        file.close()

    def show_file_use_size(self, first, second):
        shutil.copy(first, second)
        show_information(self.file_name, self.finish_version)

    def update(self):
        self.txt_space_fix()

        self.show_file_use_size(self.finish_version, self.before_update)

        self.check()

        self.update_save()

        self.show_file_use_size(self.after_update, self.finish_version)

    def update_save(self):
        with open(self.after_update, "wb") as file:
            file.write(self.content)


def main():
    Content().update()

if __name__ == '__main__':
    main()
