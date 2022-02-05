import csv
import os
import requests
import CategoryPage
import lxml
import cchardet
from bs4 import BeautifulSoup


def create_csv_files_directory(main_directory):
    csv_files_directory = main_directory + "/csvFiles/"
    os.makedirs(csv_files_directory, exist_ok=True)
    return csv_files_directory


def create_pictures_directory(main_directory):
    pictures_directory = main_directory + "/pictures/"
    os.makedirs(pictures_directory, exist_ok=True)
    return pictures_directory


def create_all_the_useful_directories():
    os.chdir('../')
    main_directory = os.getcwd()
    csv_files_directory = create_csv_files_directory(main_directory)
    pictures_directory = create_pictures_directory(main_directory)
    return {"csv_files_directory": csv_files_directory, "pictures_directory": pictures_directory}


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
    print("Starting web scraping of the web page : https://books.toscrape.com/index.html")
    useful_directories = create_all_the_useful_directories()
    csv_files_directory = useful_directories["csv_files_directory"]
    pictures_directory = useful_directories["pictures_directory"]
    session = requests.Session()
    books_toscrape_html_page = session.get("https://books.toscrape.com/index.html")
    web_html_page_soup = BeautifulSoup(books_toscrape_html_page.content, 'lxml')
    all_categories_html_objects = web_html_page_soup.find('ul', class_='nav nav-list').ul.find_all('li')
    for category_html_object in all_categories_html_objects:
        category_name = category_html_object.a.string.strip()
        print(f"Starting web scraping for the category {category_name} ...")
        pictures_directory_for_one_category = create_directory_for_one_category_pictures(category_name,
                                                                                         pictures_directory)
        csv_file_for_loading = create_csv_file_for_loading(category_name, csv_files_directory)
        book_category_url = "https://books.toscrape.com/" + category_html_object.a["href"]
        CategoryPage.extract_transform_load_all_books_infos_from_category(book_category_url, csv_file_for_loading,
                                                                          category_name,
                                                                          pictures_directory_for_one_category,
                                                                          session)

        print(f"Web scraping done for the category {category_name}")
    print("Web scraping done for the web page :  https://books.toscrape.com/index.html")


"""Starting of web scraping program"""
launch_web_scraping()
