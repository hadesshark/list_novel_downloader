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
        'Mozilla/5.0 (Windows NT 6.1) Chrome/44.0.2403.157 Safari/537.36',
        'accept-language':
        'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ja;q=0.5',
        'cookie':
        '__cfduid=de77d95c1938bd324e58a267913749ef61491283499; _td=0034978a-bf2e-4733-9267-03a90a575b8c; _ceir=1; __auc=c70c3fcd15b376c5ea8cc2bcecb; _ga=GA1.2.1418266959.1491283501; Lre7_9bf0_saltkey=I0k8d668; Lre7_9bf0_lastvisit=1515239140; Hm_lvt_a2ca3bc9ac81ca7c9ed66abd1176d6df=1515244809; Hm_lpvt_a2ca3bc9ac81ca7c9ed66abd1176d6df=1515244809; _gid=GA1.2.719788948.1515506862; datetime=113; times=111; Lre7_9bf0_forum_lastvisit=D_674_1514986092D_856_1515312019D_237_1515850427D_3419_1515854052; MCPopupClosed=yes; viewthread_datetime=114; __asc=9240519d160fef1e61c1dbd2101; cf_clearance=4e2cee0b79cfe618de35a77578ddea7353938839-1516106475-3600; Lre7_9bf0_sendmail=1; Lre7_9bf0_lastact=1516106701%09forum.php%09viewthread; Lre7_9bf0_visitedfid=3419D237D3588D3285D674; Lre7_9bf0_viewid=tid_1139773; _gat=1; _gat_n_ga=1; _gat_FictionUid_ga=1; _gat_allvip_ga=1; _gat_ckad=1; _gat_t=1; _gat_e=1; _gat_all_ga=1; _ceg.s=p2nffg; _ceg.u=p2nffg',
        'accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br'
    }

    def __init__(self, url=SettingInfo().get_url()):
        self.url = url
        self.content = ''

    def get_web_page(self):
        response = requests.get(self.url, headers=self.__headers, timeout=3)
        if response.status_code == 200:
            return etree.HTML(response.text.encode('utf-8'))
        else:
            return response.status_code

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
        self.content = Content().collect(self.info)

    def save(self):
        with open(self.save_name_and_address(), 'w', encoding='utf-8') as f:
            f.write(self.content)

    def show_title_author(self):
        self.info.show_title_author()

    def save_name_and_address(self):
        return self.file_address + self.info.__str__()


def main():
    """
    novel save -> chapter(string) collect -> from downloader(list) get page
    """
    # novel = Novel()
    # novel.show_title_author()
    # novel.save()
    downloader = Downloader()
    print(downloader.url)
    print(downloader.get_web_page())


if __name__ == '__main__':
    main()
