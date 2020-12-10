import requests
from bs4 import BeautifulSoup as bs
import csv

choice = input("Scrape a [book] [category] page : ").lower()
if choice == 'book':

    url = 'http://books.toscrape.com/catalogue/eat-fat-get-thin_688/index.html'

    response = requests.get(url) # Load the webpage content
    if response.ok: # Check if the webpage is load
        soup = bs(response.text, "lxml") # Convert the webpage to a BeautifulSoup object

        # Start extraction of the data we wanted
        prdct_pg = soup.find_all('a')[3]
        upc = soup.find_all('td')[0]
        title = soup.find('h1')
        pit = soup.find_all('td')[3]
        pet = soup.find_all('td')[2]
        num_avail = soup.find_all('td')[5]
        descr = soup.find('article', {'class': 'product_page'}).find_all('p')[3]
        cat = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2]
        revw = soup.find_all('td')[6]
        img_url = soup.find('img')

        with open('book\'s_information.csv', 'w') as p: # Open (or create if not exists) a csv file to write the data in
            # Declare the key name of the dictionnary    
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
            csv_writer.writerow({
                'product_page_url' : prdct_pg['href'].replace('..', 'http://books.toscrape.com'),
                'universal_product_code' : upc.text,
                'title' : title.text,
                'price_including_tax' : pit.text.replace('Â', ''),
                'price_excluding_tax' : pet.text.replace('Â', ''),
                'number_available' : num_avail.text.replace('In stock (', '').replace(' available)', ''),
                'product_description' : descr.text,
                'category' : cat.text,
                'review_rating' : revw.text,
                'image_url' : img_url['src'].replace('../..', 'http://books.toscrape.com')
                })
    print("File book's_information.csv  has been updated")


if choice == 'category':

    url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'

    response = requests.get(url) # Load the webpage content
    if response.ok: # Check if the webpage is load
        cat_soup = bs(response.text, "lxml") # Convert the webpage to a BeautifulSoup object


        # Get all books url
        book_urls = cat_soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})   

        links = []
        for book_url in book_urls:
            a_book = book_url.find('a')
            links.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
        print(links)

        with open('book\'s_information2.csv', 'w') as p: # Open (or create if not exists) a csv file to write the data in
            # Declare the key name of the dictionnary    
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
            for link in links:
                response = requests.get(link)
                if response.ok:
                    soup = bs(response.text, "lxml")
                    # Start extraction of the data we wanted
                    upc = soup.find_all('td')[0]
                    title = soup.find('h1')
                    pit = soup.find_all('td')[3]
                    pet = soup.find_all('td')[2]
                    num_avail = soup.find_all('td')[5]
                    descr = soup.find('article', {'class': 'product_page'}).find_all('p')[3]
                    cat = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2]
                    revw = soup.find_all('td')[6]
                    img_url = soup.find('img')
                    
                    csv_writer.writerow({
                        'product_page_url' : link,
                        'universal_product_code' : upc.text,
                        'title' : title.text,
                        'price_including_tax' : pit.text.replace('Â', ''),
                        'price_excluding_tax' : pet.text.replace('Â', ''),
                        'number_available' : num_avail.text.replace('In stock (', '').replace(' available)', ''),
                        'product_description' : descr.text,
                        'category' : cat.text,
                        'review_rating' : revw.text,
                        'image_url' : img_url['src'].replace('../..', 'http://books.toscrape.com')
                        })
            print("File book's_information2.csv  has been updated")