import BookPage
from bs4 import BeautifulSoup
import requests

def extract_transform_load_one_book_infos(book, nameFile):
    book = book.article.h3.a["href"]
    book = book.split("/")
    del book[0:3]
    book = "https://books.toscrape.com/catalogue/" + "/".join(book)
    print(f"the link of the book is : {book}")
    BookPage.extract_transform_load_all_infos_in_csv(book, nameFile)

def extract_transform_load_all_books_infos_from_category(category, nameFile):
    pageHtmlCategoriePoetry = requests.get(category)
    soupCategory = BeautifulSoup(pageHtmlCategoriePoetry.content, 'html.parser')
    redo = True
    while(redo):
        allBooksOfCategory=soupCategory.find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
        for book in allBooksOfCategory:
            extract_transform_load_one_book_infos(book, nameFile)
        pager = soupCategory.find('ul', class_="pager")
        if (pager and pager.find('li', class_="next")):
            redo = True
            categorywithoutHtmlIndex = category
            categorywithoutHtmlIndex = categorywithoutHtmlIndex.split('/')
            del categorywithoutHtmlIndex[-1]
            categoryHtmlPage = "/".join(categorywithoutHtmlIndex)
            numberOfPageshtml = pager.find('li', class_="current").string
            print(numberOfPageshtml.strip()[-1])

            link = categoryHtmlPage + "/" + pager.find('li', class_="next").a["href"]
            print(link)
            pageHtmlCategorieNextPage = requests.get(link)
            soupCategory = BeautifulSoup(pageHtmlCategorieNextPage.content, 'html.parser')
        else:
            redo = False