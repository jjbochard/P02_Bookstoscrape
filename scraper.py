# sourcery skip: for-index-underscore
import requests
from bs4 import BeautifulSoup as bs
import csv
import time

choice = input("Scrape [book] [category] [all] page : ").lower()
if choice == 'book':
    url = 'https://books.toscrape.com/catalogue/eat-fat-get-thin_688/index.html'
    # Load the webpage content
    response = requests.get(url)
    # Check if the webpage is load
    if response.ok:
        # Convert the webpage to a BeautifulSoup object
        soup = bs(response.text, "lxml")
        # Start extraction of the data we wanted
        prdct_pg = soup.find_all('a')[3]
        upc = soup.find_all('td')[0]
        title = soup.find('h1')
        pit = soup.find_all('td')[3]
        pet = soup.find_all('td')[2]
        num_avail = soup.find_all('td')[5]
        descr = soup.find('article', {'class': 'product_page'}).find_all('p')[3]
        descr = descr.text
        cat = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2]
        revws_str = soup.find('div', {'class': 'col-sm-6 product_main'}).find_all('p')[2]
        # Create a list to convert revws_str (string) into reviews_int (int)
        i = 0
        convert_revws = [None, 'One', 'Two', 'Three', 'Four', 'Five']
        # For each i (from 0 to 5), we check if revws_str == convert_revws[i]
        # i allows to navigate through index and to know the value of convert_str        
        for i in range (6):
            if revws_str['class'][1] == convert_revws[i]:
                revws_int = i
                break
            else:
                i += 1
        img_url = soup.find('img')

        # Open (or create if not exists) a csv file to write the data in
        with open('book\'s_information.csv', 'w') as p:
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
                'product_description' : descr.strip(),
                'category' : cat.text,
                'review_rating' : revws_int,
                'image_url' : img_url['src'].replace('../..', 'http://books.toscrape.com')
                })
    print("File book's_information.csv has been updated")
    response = requests.get("" + img_url['src'].replace('../..', 'http://books.toscrape.com') + "")
    file = open(title.text.replace('/', '') + ".jpg", "wb")
    file.write(response.content)
    file.close()

if choice == 'category':
    url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'

    # List of each urls' book of category page(s)
    books_links = []
    # Load the webpage content
    response = requests.get(url)
    # Check if the webpage is load
    if response.ok:
        # Convert the webpage to a BeautifulSoup object
        cat_soup = bs(response.text, "lxml")
        # Check if there is pagination for a book's category
        cat_pagination = cat_soup.find('li', {'class': 'current'})
        # If there is only one page of books in a book's category
        if cat_pagination is None:
            # Contains all book's url(not complete) for a category page
            book_urls = cat_soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
            # Iterate in the url's book to get their full url
            for book_url in book_urls:
                a_book = book_url.find('a')
                books_links.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
        # If a book's category countains several page of books
        else:
            num_pagination = int(cat_pagination.text.strip().replace('Page 1 of ', ''))
            # List of all urls for a book's category wich countains several pages
            cat_urls = []
            j = 1
            # Iterate in all pages of a book's category to get their full url
            for i in range(num_pagination):
                cat_urls.append(url.replace('index.html', 'page-') + str(j) + '.html')
                j += 1
            # Iterate in all full category urls to get all book's url
            for cat_url in cat_urls:
                # Load the webpage content
                response = requests.get(cat_url)
                # Check if the webpage is load
                if response.ok:
                    # Convert the webpage to a BeautifulSoup object
                    cat_soup = bs(response.text, "lxml")
                    # Contains all book's url(not complete) for a book's category
                    book_urls = cat_soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
                    # Iterate in the url's book to get their full url
                    for book_url in book_urls:
                        a_book = book_url.find('a')
                        books_links.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))

        # Open (or create if not exists) a csv file to write the data in
        with open('book\'s_information_category.csv', 'w') as p:
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
            # Iterate in all links to scrape the datas we want
            l =0
            for books_link in books_links:
                response = requests.get(books_link)
                if response.ok:
                    soup = bs(response.text, "lxml")
                    # Start extraction of the data we want
                    upc = soup.find_all('td')[0]
                    title = soup.find('h1')
                    pit = soup.find_all('td')[3]
                    pet = soup.find_all('td')[2]
                    num_avail = soup.find_all('td')[5]
                    descr = soup.find('article', {'class': 'product_page'}).find_all('p')[3]
                    descr = descr.text
                    cat = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2]
                    revws_str = soup.find('div', {'class': 'col-sm-6 product_main'}).find_all('p')[2]
                    # Create a list to convert revws_str (string) into reviews_int (int)
                    i = 0
                    convert_revws = [None, 'One', 'Two', 'Three', 'Four', 'Five']
                    # For each i (from 0 to 5), we check if revws_str == convert_revws[i]
                    # i allows to navigate through index and to know the value of convert_str        
                    for i in range (6):
                        if revws_str['class'][1] == convert_revws[i]:
                            revws_int = i
                            break
                        else:
                            i += 1
                    img_url = soup.find('img')
                    csv_writer.writerow({
                        'product_page_url' : books_link,
                        'universal_product_code' : upc.text,
                        'title' : title.text,
                        'price_including_tax' : pit.text.replace('Â', ''),
                        'price_excluding_tax' : pet.text.replace('Â', ''),
                        'number_available' : num_avail.text.replace('In stock (', '').replace(' available)', ''),
                        'product_description' : descr.strip(),
                        'category' : cat.text,
                        'review_rating' : revws_int,
                        'image_url' : img_url['src'].replace('../..', 'http://books.toscrape.com')
                        })
                    response = requests.get("" + img_url['src'].replace('../..', 'http://books.toscrape.com') + "")
                    file = open(title.text + ".jpg", "wb")
                    file.write(response.content)
                    file.close()
                    l += 1
                    print(l)
            print("File book's_information_category.csv has been updated")

if choice == 'all':
    #Start timer
    start_time = time.time()

    url = 'http://books.toscrape.com/'
    # List of each book url
    all_urls = []
    # List of each category url
    category_links = []
    # Load the webpage content
    response = requests.get(url)
    # Check if the webpage is load
    if response.ok:
        # Convert the webpage to a BeautifulSoup object
        all_soup = bs(response.text, "lxml")
        category_urls = all_soup.find('ul', {'class': 'nav nav-list'}).find('li').find_all('li')
        # Iterate for all category_urls to get full category url
        for category_url in category_urls:
            a_category = category_url.find('a')
            category_links.append('http://books.toscrape.com/' + a_category['href'])
        # Iterate for each category_links to get all book's url
        # k = 1
        for category_link in category_links:

            # List of each urls' book of category page(s)
            links = []
            # Load the webpage content
            response = requests.get(category_link)
            # Check if the webpage is load
            if response.ok:
                # Convert the webpage to a BeautifulSoup object
                cat_soup = bs(response.text, "lxml")
                # Check if there is pagination for a book's category
                cat_pagination = cat_soup.find('li', {'class': 'current'})
                # If there is only one page of books in a book's category
                if cat_pagination is None:
                    # Contains all book's url(not complete) for a category page
                    book_urls = cat_soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
                    # Iterate in the url's book to get their full url
                    for book_url in book_urls:
                        a_book = book_url.find('a')
                        links.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
                        all_urls.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
                # If a book's category countains several page of books
                else:
                    num_pagination = int(cat_pagination.text.strip().replace('Page 1 of ', ''))
                    # List of all urls for a book's category wich countains several pages
                    cat_urls = []
                    j = 1
                    # Iterate in all pages of a book's category to get their full url
                    for i in range(num_pagination):
                        cat_urls.append(category_link.replace('index', 'page-' + str(j)))
                        j += 1
                    # Iterate in all full category urls to get all book's url
                    for cat_url in cat_urls:
                        # Load the webpage content
                        response = requests.get(cat_url)
                        # Check if the webpage is load
                        if response.ok:
                            # Convert the webpage to a BeautifulSoup object
                            cat_soup = bs(response.text, "lxml")
                            # Contains all book's url(not complete) for a book's category
                            book_urls = cat_soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
                            # Iterate in the url's book to get their full url
                            for book_url in book_urls:
                                a_book = book_url.find('a')
                                links.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
                                all_urls.append(a_book['href'].replace('../../..', 'http://books.toscrape.com/catalogue'))
                for link in links:
                    response = requests.get(link)
                    if response.ok:
                        soup = bs(response.text, "lxml")
                        # Start extraction of the data we want
                        cat = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2]                
                with open(cat.text.replace(' ', '_') + ".csv", 'w') as p:
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
                    l = 0
                    for link in links:                
                        response = requests.get(link)
                        if response.ok:
                            soup = bs(response.text, "lxml")
                            # Start extraction of the data we want
                            upc = soup.find_all('td')[0]
                            title = soup.find('h1')
                            pit = soup.find_all('td')[3]
                            pet = soup.find_all('td')[2]
                            num_avail = soup.find_all('td')[5]
                            descr = soup.find('article', {'class': 'product_page'}).find_all('p')[3]
                            descr = descr.text
                            cat = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2]
                            revws_str = soup.find('div', {'class': 'col-sm-6 product_main'}).find_all('p')[2]
                            # Create a list to convert revws_str (string) into reviews_int (int)
                            i = 0
                            convert_revws = [None, 'One', 'Two', 'Three', 'Four', 'Five']
                            # For each i (from 0 to 5), we check if revws_str == convert_revws[i]
                            # i allows to navigate through index and to know the value of convert_str        
                            for i in range (6):
                                if revws_str['class'][1] == convert_revws[i]:
                                    revws_int = i
                                    break
                                else:
                                    i += 1
                            img_url = soup.find('img')
                                    
                            # Open (or create if not exists) a csv file to write the data in
                        # Iterate in all links to scrape the datas we want
                    
                    
                        # response = requests.get("" + img_url['src'].replace('../..', 'http://books.toscrape.com') + "")
                                
                
                            csv_writer.writerow({
                                'product_page_url' : link,
                                'universal_product_code' : upc.text,
                                'title' : title.text,
                                'price_including_tax' : pit.text.replace('Â', ''),
                                'price_excluding_tax' : pet.text.replace('Â', ''),
                                'number_available' : num_avail.text.replace('In stock (', '').replace(' available)', ''),
                                'product_description' : descr.strip(),
                                'category' : cat.text,
                                'review_rating' : revws_int,
                                'image_url' : img_url['src'].replace('../..', 'http://books.toscrape.com')
                                })
                            response = requests.get("" + img_url['src'].replace('../..', 'http://books.toscrape.com') + "")
                            file = open(title.text.replace('/', '') + ".jpg", "wb")
                            file.write(response.content)
                            file.close()
                            l += 1
                            print(l)
            print("File " + cat.text.replace(' ', '_') + ".csv has been updated")      
    interval = time.time() - start_time
    print(interval, " seconds")