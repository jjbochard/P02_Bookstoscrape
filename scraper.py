# -*- coding: utf-8 -*-
import csv
import time
import requests
from bs4 import BeautifulSoup as bs
import function

choice = input("Scrape [book] [category] [all] page : ").lower()
if choice == 'book':

    data = function.get_books_informations(
        'http://books.toscrape.com/catalogue/eat-fat-get-thin_688/index.html'
        )
    function.write_csv('book\'s_information.csv', data)
    function.download_image(data)

if choice == 'category':

    books_links = function.get_url_books_for_a_category_page(
        'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
        )
    with open('book\'s_information_category.csv', 'w') as p:
        fnames = [
            'product_page_url',
            'universal_product_code',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url'
            ]
        csv_writer = csv.DictWriter(p, delimiter='|', fieldnames=fnames)
        csv_writer.writeheader()
        for books_link in books_links:
            data = function.get_books_informations(books_link)
            csv_writer.writerow({
                'product_page_url' : data['product_page_url'],
                'universal_product_code' : data['universal_product_code'].text,
                'title' : data['title'].text,
                'price_including_tax' :data['price_including_tax'].text.replace('Â', ''),
                'price_excluding_tax' : data['price_excluding_tax'].text.replace('Â', ''),
                'number_available' : data['number_available'].text.replace('In stock (', '').replace(' available)', ''),
                'product_description' : data['product_description'].text,
                'category' : data['category'].text,
                'review_rating' : data['review_rating'],
                'image_url' : data['image_url']['src'].replace('../..', 'http://books.toscrape.com')
                })
            response = requests.get("" + data['image_url']['src'].replace('../..', 'http://books.toscrape.com') + "")
            function.download_image(data)
    print("File book's_information_category.csv has been updated")

if choice == 'all':
    start_time = time.time()
    k = 0
    category_links = function.get_all_url_category()
    for category_link in category_links:
        books_category_name = function.get_books_category_name(category_link)
        books_links = function.get_url_books_for_a_category_page(category_link)
        with open(books_category_name.replace(' ', '_') + ".csv", 'w') as p:
            fnames = [
                'product_page_url',
                'universal_product_code',
                'title',
                'price_including_tax',
                'price_excluding_tax',
                'number_available',
                'product_description',
                'category',
                'review_rating',
                'image_url'
                ]
            csv_writer = csv.DictWriter(p, delimiter='|', fieldnames=fnames)
            csv_writer.writeheader()

            for books_link in books_links:
                data = function.get_books_informations(books_link)
                csv_writer.writerow({
                'product_page_url' : data['product_page_url'],
                'universal_product_code' : data['universal_product_code'].text,
                'title' : data['title'].text,
                'price_including_tax' :data['price_including_tax'].text.replace('Â', ''),
                'price_excluding_tax' : data['price_excluding_tax'].text.replace('Â', ''),
                'number_available' : data['number_available'].text.replace('In stock (', '').replace(' available)', ''),
                'product_description' : data['product_description'].text,
                'category' : data['category'].text,
                'review_rating' : data['review_rating'],
                'image_url' : data['image_url']['src'].replace('../..', 'http://books.toscrape.com')
                })
                function.download_image(data)
                k += 1
                print(k)
        print("File " + books_category_name.replace(' ', '_') + ".csv has been updated")
    interval = (time.time() - start_time)
    function.print_time(interval)
