import BookPage
from bs4 import BeautifulSoup
import requests


def extract_transform_load_one_book_infos(book, nameFile, category_name, pictures_directory):
    book_page_url_from_html_page = book.h3.a["href"]
    book_page_url = book_page_url_from_html_page.replace("../../..", "https://books.toscrape.com/catalogue")
    print(f"the link of the book is : {book_page_url}")
    BookPage.extract_transform_load_all_infos_in_csv(book_page_url, nameFile, category_name, pictures_directory)


def check_if_there_is_next_page(category_soup, product_category_url):
    next_page = category_soup.find('li', class_="next")
    if next_page:
        url_of_next_page_from_html_page = next_page.a["href"]
        url_of_next_page = product_category_url.replace("index.html", url_of_next_page_from_html_page)
        next_page_html = requests.get(url_of_next_page)
        return BeautifulSoup(next_page_html.content, 'html.parser')
    else:
        return None


def extract_transform_load_all_books_infos_from_category(product_category_url, file_csv_name, category_name, pictures_directory):
    product_category_html = requests.get(product_category_url)
    category_soup = BeautifulSoup(product_category_html.content, 'html.parser')
    while (category_soup):
        all_books_category_article = category_soup.find_all('article', class_='product_pod')
        for book_article in all_books_category_article:
            extract_transform_load_one_book_infos(book_article, file_csv_name, category_name, pictures_directory)
        category_soup = check_if_there_is_next_page(category_soup, product_category_url)
