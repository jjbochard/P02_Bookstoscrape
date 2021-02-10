# P02_Bookstoscrape

## Table of contents
- [Table of content](#table-of-content)
- [Foreword](#foreword)
- [Installation](#installation)
- [How to use](#how-to-use)
- [Possible improvements](#possible-improvements)

## Foreword

The aim of this program is to scrape a site wich contains a lot of books in order to get some informations for all the books.
The information we wanted are :
- product_page_url
- universal_product_code
- price_including_tax
- price_excluding_tax
- number_available
- category
- review_rating
- image_url

When scraping all the site, the datas are writing in csv files grouping by category. The books' image are also downloading.


## Installation

### Clone the code source (using ssh)

    mkdir scraper
    git clone git@github.com:jjbochard/P02_Bookstoscrape.git scraper
    cd scraper

### Create your virtual environnement

First, install [Python 3.6+](https://www.python.org/downloads/).

Then, create your virtual environnement :

    python -m venv <your_venv_name>

Activate it :

- with bash command prompt

        source <your_venv_name>/bin/activate

- or with Windows PowerShell

        .\venv\Scripts\activate

Finally, install required modules

    pip install -r requirements.txt

To deactivate your venv :

    deactivate

## How to use

Launch a shell and type :

    python3 scraper.py

Now, you have three choices. You can :

- scrape a book's page in order to get all the informations we wanted by typing **book**
- scrape all books from a category in order to get all the informations we wanted for all the books of the category by typing **category**
- scrape all the books of all the categories in order to get all the informations we wanted for all the books of the site by typing **all**

## Possible improvements

- To run the script more efficiently, asynchronous programmation can be use by using threads.

- Because I'm using Python, I can use clasess to code with objects
