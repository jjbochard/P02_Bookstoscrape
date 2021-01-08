import requests
from bs4 import BeautifulSoup as bs
import csv

def get_books_informations (url):

    global product_page_url
    global universal_product_code
    global title
    global price_including_tax
    global price_excluding_tax
    global number_available
    global product_description
    global category
    global review_rating
    global image_url

    response = requests.get(url) # Load the webpage content
    if response.ok: # Check if the webpage is load
        soup = bs(response.text, "lxml") # Convert the webpage to a BeautifulSoup object

        # Start extraction of the data we wanted
        product_page_url = url
        universal_product_code = soup.find_all('td')[0]
        title = soup.find('h1')
        price_including_tax = soup.find_all('td')[3]
        price_excluding_tax = soup.find_all('td')[2]
        number_available = soup.find_all('td')[5]
        product_description = soup.find('article', {'class': 'product_page'}).find_all('p')[3]
        category = soup.find('ul', {'class': 'breadcrumb'}).find_all('a')[2]
        review_rating = soup.find('div', {'class': 'col-sm-6 product_main'}).find_all('p')[2]
        # Create a list to convert revws_str (string) into reviews_int (int)
        i = 0
        convert_revws = [None, 'One', 'Two', 'Three', 'Four', 'Five']
        # For each i (from 0 to 5), we check if revws_str == convert_revws[i]
        # i allows to navigate through index and to know the value of convert_str        
        for i in range (6):
            if review_rating['class'][1] == convert_revws[i]:
                review_rating = i
                break
            else:
                i += 1
        image_url = soup.find('img')
    else:
        print("Please, check for the url")


choice = input("Scrape a [book] page : ").lower()
if choice == 'book':

    get_books_informations('http://books.toscrape.com/catalogue/eat-fat-get-thin_688/index.html')

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
            'product_page_url' : product_page_url,
            'universal_product_code' : universal_product_code.text,
            'title' : title.text,
            'price_including_tax' : price_including_tax.text.replace('Â', ''),
            'price_excluding_tax' : price_excluding_tax.text.replace('Â', ''),
            'number_available' : number_available.text.replace('In stock (', '').replace(' available)', ''),
            'product_description' : product_description.text,
            'category' : category.text,
            'review_rating' : review_rating,
            'image_url' : image_url['src'].replace('../..', 'http://books.toscrape.com')
            })

    print("File book's_information.csv  has been updated")