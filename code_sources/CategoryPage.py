import BookPage
from bs4 import BeautifulSoup


def extract_transform_load_one_book_infos(book_article, csv_file_for_loading, category_name,
                                          pictures_directory_for_one_category, session):
    book_page_url_from_html_page = book_article.h3.a["href"]
    book_page_url = book_page_url_from_html_page.replace("../../..", "https://books.toscrape.com/catalogue")
    BookPage.extract_transform_load_all_infos_in_csv(book_page_url, csv_file_for_loading, category_name,
                                                     pictures_directory_for_one_category, session)


def get_next_page(book_category_soup, book_category_url, session):
    next_page = book_category_soup.find('li', class_="next")
    if next_page:
        url_of_next_page_from_html_page = next_page.a["href"]
        url_of_next_page = book_category_url.replace("index.html", url_of_next_page_from_html_page)
        next_page_html = session.get(url_of_next_page).content
        return BeautifulSoup(next_page_html, 'lxml')
    else:
        return None


def extract_transform_load_all_books_infos_from_category(book_category_url, csv_file_for_loading, category_name,
                                                         pictures_directory_for_one_category, session):
    book_category_html = session.get(book_category_url)
    book_category_soup = BeautifulSoup(book_category_html.content, 'lxml')
    while book_category_soup:
        all_books_category_articles = book_category_soup.find_all('article', class_='product_pod')
        for book_article in all_books_category_articles:
            extract_transform_load_one_book_infos(book_article, csv_file_for_loading, category_name,
                                                  pictures_directory_for_one_category, session)
        book_category_soup = get_next_page(book_category_soup, book_category_url, session)
