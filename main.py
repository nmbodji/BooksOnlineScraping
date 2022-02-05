import CategoryPage
from bs4 import BeautifulSoup
import requests
import csv
import os


def create_csv_file(nameFile):
    fieldnames = ['product_page_url', 'image_url', 'title', 'number_available', 'review_rating', 'product_description',
                  'universal_ product_code (upc)', 'price_excluding_tax',
                  'price_including_tax']
    with open(nameFile, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()


web_html_page = requests.get("https://books.toscrape.com/index.html")
soup_web_html_page = BeautifulSoup(web_html_page.content, 'html.parser')
all_html_category = soup_web_html_page.find('ul', class_='nav nav-list').ul.find_all('li')
os.mkdir("csvFiles")
for category in all_html_category:
    nameFile = category.a.string.strip() + ".csv"
    nameFile = "csvFiles/" + nameFile
    create_csv_file(nameFile)
    print(category.a.string.strip())
    product_category_url = "https://books.toscrape.com/" + category.a["href"]
    CategoryPage.extract_transform_load_all_books_infos_from_category(product_category_url, nameFile)
