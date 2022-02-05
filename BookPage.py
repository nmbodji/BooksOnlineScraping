import re
import requests
import csv
from bs4 import BeautifulSoup


def extract_and_transform_image_link(product_page_soup, product_infos_to_load):
    image_book_url_from_html_page = product_page_soup.find('img')['src']
    image_book_url_to_load = image_book_url_from_html_page.replace("../../", "https://books.toscrape.com/")
    print(f"the link of the picture is : {image_book_url_to_load}")
    product_infos_to_load["image_url"] = image_book_url_to_load


def extract_and_transform_title(product_main_infos_from_html_page, product_infos_to_load):
    title_from_html_page = product_main_infos_from_html_page.h1.string
    print(f"The title of the book is : {title_from_html_page}")
    product_infos_to_load["title"] = title_from_html_page


def extract_and_transform_stock_available(product_main_infos_from_html_page, product_infos_to_load):
    stock_available_from_html_page = product_main_infos_from_html_page.find('p', class_='instock availability').text
    stock_available_to_load = re.findall(r'\d+', stock_available_from_html_page)[0]
    print(f"The available stock is : {stock_available_to_load}")
    product_infos_to_load["number_available"] = stock_available_to_load


def extract_and_transform_rating(product_main_infos_from_html_page, product_infos_to_load):
    review_rating_from_html_page = \
        product_main_infos_from_html_page.find('p', class_=re.compile("star-rating"))["class"][1]
    print(f"The rating of the book is : {review_rating_from_html_page}")
    product_infos_to_load["review_rating"] = review_rating_from_html_page


def extract_and_transform_title_stock_available_and_rating(product_page_soup, allInfos):
    product_main_infos_from_html_page = product_page_soup.find('div', class_='col-sm-6 product_main')
    extract_and_transform_title(product_main_infos_from_html_page, allInfos)
    extract_and_transform_stock_available(product_main_infos_from_html_page, allInfos)
    extract_and_transform_rating(product_main_infos_from_html_page, allInfos)


def extract_and_transform_description(product_page_soup, product_infos_to_load):
    description_section_from_html_page = product_page_soup.find('div', id='product_description', class_="sub-header")
    if description_section_from_html_page:
        product_description_from_html_page = description_section_from_html_page.findNext("p").string
        print(f"The description of the book is : {product_description_from_html_page}")
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


def load_infos_in_csv(product_infos_to_load, file_csv_name, category_name):
    fieldnames = ['product_page_url', 'image_url', 'title', 'number_available', 'review_rating', 'product_description',
                  'universal_ product_code (upc)', 'price_excluding_tax', 'price_including_tax']
    with open(file_csv_name, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(product_infos_to_load)

    transformed_title = product_infos_to_load['title'].replace("/", "-")
    filename = category_name + '/' + transformed_title + '.jpg'
    with open(filename, 'wb') as file:
        response = requests.get(product_infos_to_load['image_url'])
        file.write(response.content)


def extract_and_transform_infos_from_html_page(product_infos_to_load, product_page_url):
    product_page_html = requests.get(product_page_url)
    product_page_soup = BeautifulSoup(product_page_html.content, 'html.parser')
    extract_and_transform_image_link(product_page_soup, product_infos_to_load)
    extract_and_transform_title_stock_available_and_rating(product_page_soup, product_infos_to_load)
    extract_and_transform_description(product_page_soup, product_infos_to_load)
    extract_and_transform_upc_and_price(product_page_soup, product_infos_to_load)


def extract_transform_load_all_infos_in_csv(product_page_url, file_csv_name, category_name):
    product_infos_to_load = {"product_page_url": product_page_url}
    extract_and_transform_infos_from_html_page(product_infos_to_load, product_page_url)
    load_infos_in_csv(product_infos_to_load, file_csv_name, category_name)
