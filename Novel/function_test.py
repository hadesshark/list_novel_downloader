# -*- coding: utf-8 -*-
# gui 版本
# 主畫面 書庫頁
# 顯示書籍資料

# 功能
## 新增書籍
## 跳出 diaolod

## 設定書籍基本資料

from Book import Book
from Bookstore import Bookstore

title = None
author = None
url = None
finish = None
book = Book()
book.set_info(title, author, url, finish)

## 判斷書庫中是否有這本書
bookstore = Bookstore()
if not bookstore.check_have(book):
    ## 如果 沒有 增加這本書
    bookstore.add_book(book)

# finish
"""
希望有設定後有跑馬燈效果
"""
## 在線閱讀


# 書籍更新（全部更新）/（個別更新）
## 個別更新
## 書籍判斷是否有新的章節

## 如果 有 就更新

## finish

## 全部更新
## 書庫中的書判斷是否有新的章節

## 有 就更新書籍

## finish
# finish
