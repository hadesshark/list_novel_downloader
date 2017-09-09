import json


with open("book_list.json", encoding="utf-8") as book_list:
    bookstore_list = json.load(book_list)

with open("Book.json", encoding="utf-8") as book:
    book_info = json.load(book)

data = bookstore_list
if data["novel"] == []:
    print(data)
    print(data["novel"].insert(0, book_info))
    print(data)

    with open("book_list.json", mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2)
