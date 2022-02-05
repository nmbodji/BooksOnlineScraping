import re
import csv
from bs4 import BeautifulSoup


def extract_and_transform_image_link(product_page_soup, product_infos_to_load):
    image_book_url_from_html_page = product_page_soup.find('img')['src']
    image_book_url_to_load = image_book_url_from_html_page.replace("../../", "https://books.toscrape.com/")
    product_infos_to_load["image_url"] = image_book_url_to_load


def extract_and_transform_title(product_main_infos_from_html_page, product_infos_to_load):
    title_from_html_page = product_main_infos_from_html_page.h1.string
    product_infos_to_load["title"] = title_from_html_page


def extract_and_transform_stock_available(product_main_infos_from_html_page, product_infos_to_load):
    stock_available_from_html_page = product_main_infos_from_html_page.find('p', class_='instock availability').text
    stock_available_to_load = re.findall(r'\d+', stock_available_from_html_page)[0]
    product_infos_to_load["number_available"] = stock_available_to_load


def extract_and_transform_rating(product_main_infos_from_html_page, product_infos_to_load):
    review_rating_from_html_page = \
    product_main_infos_from_html_page.find('p', class_=re.compile("star-rating"))["class"][1]
    product_infos_to_load["review_rating"] = review_rating_from_html_page


def extract_and_transform_title_stock_available_and_rating(product_page_soup, product_infos_to_load):
    product_main_infos_from_html_page = product_page_soup.find('div', class_='col-sm-6 product_main')
    extract_and_transform_title(product_main_infos_from_html_page, product_infos_to_load)
    extract_and_transform_stock_available(product_main_infos_from_html_page, product_infos_to_load)
    extract_and_transform_rating(product_main_infos_from_html_page, product_infos_to_load)


def extract_and_transform_description(product_page_soup, product_infos_to_load):
    description_section_from_html_page = product_page_soup.find('div', id='product_description', class_="sub-header")
    if description_section_from_html_page:
        product_description_from_html_page = description_section_from_html_page.findNext("p").string
        product_infos_to_load["product_description"] = product_description_from_html_page
    else:
        product_infos_to_load["product_description"] = "none"


def extract_and_transform_upc_and_price(product_page_soup, product_infos_to_load):
    product_infos_table_from_html_page = product_page_soup.find('table', class_="table table-striped").find_all('tr')
    for product_info in product_infos_table_from_html_page:
        name_info = product_info.th.string
        value_info = product_info.td.string
        if name_info == "UPC":
            product_infos_to_load["universal_ product_code (upc)"] = value_info
        elif name_info == "Price (excl. tax)":
            product_infos_to_load["price_excluding_tax"] = value_info
        elif name_info == "Price (incl. tax)":
            product_infos_to_load["price_including_tax"] = value_info


def load_book_picture(product_infos_to_load, pictures_directory_for_one_category, session):
    transformed_title = product_infos_to_load['title'].replace("/", "-")
    filename = pictures_directory_for_one_category + transformed_title + '.jpg'
    with open(filename, 'wb') as file:
        response = session.get(product_infos_to_load['image_url'])
        file.write(response.content)


def load_book_informations(csv_file_for_loading, product_infos_to_load):
    fieldnames = ['product_page_url',
                  'universal_ product_code (upc)',
                  'title',
                  'price_including_tax',
                  'price_excluding_tax',
                  'number_available',
                  'product_description',
                  'category',
                  'review_rating',
                  'image_url']
    with open(csv_file_for_loading, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(product_infos_to_load)


def load_in_csv(product_infos_to_load, csv_file_for_loading, pictures_directory_for_one_category, session):
    load_book_informations(csv_file_for_loading, product_infos_to_load)
    load_book_picture(product_infos_to_load, pictures_directory_for_one_category, session)


def extract_and_transform_infos_from_html_page(product_infos_to_load, book_page_url, session):
    product_page_html = session.get(book_page_url)
    product_page_soup = BeautifulSoup(product_page_html.content, 'lxml')
    extract_and_transform_image_link(product_page_soup, product_infos_to_load)
    extract_and_transform_title_stock_available_and_rating(product_page_soup, product_infos_to_load)
    extract_and_transform_description(product_page_soup, product_infos_to_load)
    extract_and_transform_upc_and_price(product_page_soup, product_infos_to_load)


def extract_transform_load_all_infos_in_csv(book_page_url, csv_file_for_loading, category_name,
                                            pictures_directory_for_one_category, session):
    product_infos_to_load = {"product_page_url": book_page_url, "category": category_name}
    extract_and_transform_infos_from_html_page(product_infos_to_load, book_page_url, session)
    load_in_csv(product_infos_to_load, csv_file_for_loading, pictures_directory_for_one_category, session)
