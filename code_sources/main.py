import CategoryPage
from bs4 import BeautifulSoup
import requests
import csv
import os

def create_all_the_useful_directories():
    os.chdir('../')
    main_directory = os.getcwd()
    csv_files_directory = create_csv_files_directory(main_directory)
    pictures_directory = create_pictures_directory(main_directory)
    return {"csv_files_directory": csv_files_directory, "pictures_directory": pictures_directory}


def create_csv_files_directory(main_directory):
    csv_files_directory = main_directory + "/csvFiles/"
    os.makedirs(csv_files_directory, exist_ok=True)
    return csv_files_directory


def create_pictures_directory(main_directory):
    pictures_directory = main_directory + "/pictures/"
    os.makedirs(pictures_directory, exist_ok=True)
    return pictures_directory


def create_directory_for_one_category_pictures(category_name, pictures_directory):
    pictures_directory_for_one_category = pictures_directory + category_name + '/'
    os.makedirs(pictures_directory_for_one_category, exist_ok=True)
    return pictures_directory_for_one_category


def create_csv_file_for_loading(category_name, csv_files_directory):
    csv_file_for_loading = csv_files_directory + category_name + ".csv"
    fieldnames = ['product_page_url', 'image_url', 'title', 'number_available', 'review_rating', 'product_description',
                  'universal_ product_code (upc)', 'price_excluding_tax',
                  'price_including_tax']
    with open(csv_file_for_loading, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
    return csv_file_for_loading


def launch_web_scraping():
    useful_directories = create_all_the_useful_directories()
    csv_files_directory = useful_directories["csv_files_directory"]
    pictures_directory = useful_directories["pictures_directory"]
    books_toscrape_html_page = requests.get("https://books.toscrape.com/index.html")
    soup_web_html_page = BeautifulSoup(books_toscrape_html_page.content, 'html.parser')
    all_categories_html_objects = soup_web_html_page.find('ul', class_='nav nav-list').ul.find_all('li')
    for category_html_object in all_categories_html_objects:
        category_name = category_html_object.a.string.strip()
        pictures_directory_for_one_category = create_directory_for_one_category_pictures(category_name,
                                                                                         pictures_directory)
        csv_file_for_loading = create_csv_file_for_loading(category_name, csv_files_directory)
        print(category_name)
        product_category_url = "https://books.toscrape.com/" + category_html_object.a["href"]
        CategoryPage.extract_transform_load_all_books_infos_from_category(product_category_url, csv_file_for_loading,
                                                                          category_name,
                                                                          pictures_directory_for_one_category)


launch_web_scraping()
