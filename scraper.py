# -*- coding: utf-8 -*-

import time

import function

choice = input("Scrape [book] [category] [all] page : ").lower()
if choice == "book":
    book = []
    data = function.get_book_informations(
        "http://books.toscrape.com/catalogue/red-hoodarsenal-vol-1-open-for-business-red-hoodarsenal-1_729/index.html"
    )
    book.append(data)
    function.write_csv(book, "book_information.csv")
    function.download_image(data)

if choice == "c":

    book_links = function.get_url_books_for_a_category_page(
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    )

    books = []
    for book_link in book_links:
        data = function.get_book_informations(book_link)
        function.download_image(data)
        books.append(data)
    function.write_csv(books, "book's_information_category.csv")

    print("File book's_information_category.csv has been updated")

if choice == "all":
    start_time = time.time()
    k = 0
    books = []
    category_links = function.get_all_url_category()
    for category_link in category_links:
        books_category_name = function.get_books_category_name(category_link)
        book_links = function.get_url_books_for_a_category_page(category_link)
        for book_link in book_links:
            data = function.get_book_informations(book_link)
            function.download_image(data)
            books.append(data)
            k += 1
            print(k)
        function.write_csv(books, books_category_name + ".csv")
        print("File " + books_category_name + ".csv has been updated")
    interval = time.time() - start_time
    function.print_time(interval)
