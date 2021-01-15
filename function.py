# -*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup as bs

def get_books_informations(url):

    data = {}

    response = requests.get(url)
    if response.ok:
        soup = bs(response.text, "lxml")

        data['product_page_url'] = url
        data['universal_product_code'] = soup.find_all('td')[0]
        data['title'] = soup.find('h1')
        data['price_including_tax'] = soup.find_all('td')[3]
        data['price_excluding_tax'] = soup.find_all('td')[2]
        data['number_available'] = soup.find_all('td')[5]
        data['product_description'] = soup.find('article', {'class': 'product_page'}).find_all('p')[3]
        data['category'] = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2]
        data ['review_rating'] = soup.find('div', {'class': 'col-sm-6 product_main'}).find_all('p')[2]
        i = 0
        convert_revws = [None, 'One', 'Two', 'Three', 'Four', 'Five']
        for i in range(6):
            if data['review_rating']['class'][1] == convert_revws[i]:
                data['review_rating'] = i
                break
            else:
                i += 1
        data['image_url'] = soup.find('img')
    return data

def write_csv(csv_name, file):
    with open(csv_name, 'w') as p:
        fnames = []
        for key in file.keys():
            fnames.append(key)
        csv_writer = csv.DictWriter(p, delimiter='|', fieldnames=fnames)
        csv_writer.writeheader()
        csv_writer.writerow({
            'product_page_url' : file['product_page_url'],
            'universal_product_code' : file['universal_product_code'].text,
            'title' : file['title'].text,
            'price_including_tax' :file['price_including_tax'].text.replace('Â', ''),
            'price_excluding_tax' : file['price_excluding_tax'].text.replace('Â', ''),
            'number_available' : file['number_available'].text.replace('In stock (', '').replace(' available)', ''),
            'product_description' : file['product_description'].text,
            'category' : file['category'].text,
            'review_rating' : file['review_rating'],
            'image_url' : file['image_url']['src'].replace('../..', 'http://books.toscrape.com')
            })
    print("File " + csv_name + " has been updated")

def download_image(file):
    response = requests.get("" + file['image_url']['src'].replace('../..', 'http://books.toscrape.com') + "")
    with open(file['title'].text.replace('/', '') + ".jpg", "wb") as file:
        file.write(response.content)
        file.close()

def get_url_books_for_a_category_page(url):
    books_links = []
    response = requests.get(url)
    if response.ok:
        soup = bs(response.text, "lxml")
        category_pagination = soup.find('li', {'class': 'current'})
        if category_pagination is None:
            book_urls = soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
            for book_url in book_urls:
                a_book = book_url.find('a')
                books_links.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
        else:
            num_pagination = int(category_pagination.text.strip().replace('Page 1 of ', ''))
            category_urls = []
            j = 1
            for i in range(num_pagination):
                category_urls.append(url.replace('index.html', 'page-') + str(j) + '.html')
                j += 1
            for category_url in category_urls:
                response = requests.get(category_url)
                if response.ok:
                    soup = bs(response.text, "lxml")
                    book_urls = soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
                    for book_url in book_urls:
                        a_book = book_url.find('a')
                        books_links.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
    return books_links

def get_all_url_category():

    category_links = []
    url = 'http://books.toscrape.com/'
    response = requests.get(url)
    if response.ok:
        soup = bs(response.text, "lxml")
        category_urls = soup.find('ul', {'class': 'nav nav-list'}).find('li').find_all('li')
        for category_url in category_urls:
            a_category = category_url.find('a')
            category_links.append('http://books.toscrape.com/' + a_category['href'])
    return category_links

def get_books_category_name(url_books_category):
    books_category_name = url_books_category.replace('http://books.toscrape.com/catalogue/category/books/', '').replace('/index.html', '').split("_")
    books_category_name = books_category_name[0].replace("-", " ").capitalize()
    return books_category_name


def print_time(raw_interval):
    interval_in_min = raw_interval /60
    extra_sec = round(interval_in_min % 1, 2)
    interval_in_sec = round(extra_sec * 60)
    print("The site has been scraped in " + str(round(interval_in_min)) + " minutes et " + str(interval_in_sec) + " seconds.")