# 設定書籍資料用來下載

import sys
sys.path.append("../../")

from Novel.Book import Book

book = Book()
book = Book().set_info("title", "author", "url", "finish")
# print(book.all_books())
