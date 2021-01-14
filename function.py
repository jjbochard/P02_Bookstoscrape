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
