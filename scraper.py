# -*- coding: utf-8 -*-
import csv
import time
import function

choice = input("Scrape [book] page : ").lower()
if choice == 'book':

    data = function.get_books_informations(
        'http://books.toscrape.com/catalogue/eat-fat-get-thin_688/index.html'
        )
    function.write_csv('book\'s_information.csv', data)
    function.download_image(data)
