# -*- coding: utf-8 -*-

import concurrent.futures
import time

import function

choice = input("Scrape [book] [category] [all] page : ").lower()
if choice == "book":
    book = []
    data = function.get_book_informations(
        "http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html"
    )
    book.append(data)
    function.write_csv(book, "book_information.csv")
    function.download_image(data, "")

if choice == "category":

    book_links = function.get_url_books_for_a_category_page(
        "http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"
    )

    books = []
    for book_link in book_links:
        data = function.get_book_informations(book_link)
        function.download_image(data)
        books.append(data, "")
    function.write_csv(books, "book's_information_category.csv")

    print("File book's_information_category.csv has been updated")

if choice == "all":

    def scrap_site(category_link):
        books = []
        books_category_name = function.get_books_category_name(category_link)
        book_links = function.get_url_books_for_a_category_page(category_link)
        for book_link in book_links:
            data = function.get_book_informations(book_link)
            function.download_image(data, "img/")
            books.append(data)
        function.write_csv(books, "csv/" + books_category_name + ".csv")
        print("File " + books_category_name + ".csv has been updated")

    start_time = time.time()
    category_links = function.get_all_url_category()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrap_site, category_links)

    interval = time.time() - start_time
    function.print_time(interval)
