# -*- coding: utf-8 -*-
import pytest

from test2 import Book, Bookstore
from JsonInit import JsonFile

@pytest.fixture
def book():
    return Book()

@pytest.fixture
def jsonbook():
    return JsonFile()

def test_book_title(book, jsonbook):
    assert book.get_title() == jsonbook.get_title()


def test_book_save_title(book, jsonbook):
    assert book.get_save_title() == jsonbook.__str__()



@pytest.fixture
def bookstore():
    return Bookstore()


def test_len_book_list(bookstore):
    assert len(bookstore.get_book_list()) == 74
