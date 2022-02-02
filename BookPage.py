import re
import requests
import csv
from bs4 import BeautifulSoup

def extract_and_transform_image_link(soup, allInfos):
	imageBookHtml=soup.find('img')
	imageBook = imageBookHtml['src']
	imageBook = imageBook.split("/")
	del imageBook[0:2]
	imageBook = "https://books.toscrape.com/" + "/".join(imageBook)
	print(f"the link of the picture is : {imageBook}")
	allInfos["Image_url"] = imageBook

def extract_and_transform_title(infos, allInfos):
	title = infos.h1.string
	print(f"The title of the book is : {title}")
	allInfos["Title"] = title

def extract_and_transform_stock_available(infos, allInfos):
	stockHtml = infos.find('p', class_ = 'instock availability')
	stock = stockHtml.text.strip().split()[2]
	stock = stock.replace('(', '')
	print(f"The available stock is : {stock}")
	allInfos["Stock"] = stock

def extract_and_transform_rating(infos, allInfos):
	ratinghtml = infos.find('p', class_ = re.compile("star-rating"))
	rating = ratinghtml["class"][1]
	print(f"The rating of the book is : {rating}")
	allInfos["Rating"] = rating

def extract_and_transform_title_stock_available_and_rating(soup, allInfos):
	infos = soup.find('div', class_='col-sm-6 product_main')
	extract_and_transform_title(infos, allInfos)
	extract_and_transform_stock_available(infos, allInfos)
	extract_and_transform_rating(infos, allInfos)

def extract_and_transform_description(soup, allInfos):
	headerDescriptionhtml = soup.find('div', id='product_description', class_="sub-header")
	if headerDescriptionhtml:
		description = headerDescriptionhtml.findNext("p").string
		print(f"The description of the book is : {description}")
		allInfos["Description"] = description
	else:
		allInfos["Description"] = "none"

def extract_and_transform_upc_and_price(soup, allInfos):
	table = soup.find('table', class_="table table-striped")
	addInfos = table.find_all('tr')
	for info in addInfos:
		if info.th.string == "UPC" or info.th.string == "Price (excl. tax)" or info.th.string == "Price (incl. tax)":
			allInfos[info.th.string] = info.td.string

def load_infos_in_csv(allInfos, nameFile):
	fieldnames = ['Image_url', 'Title', 'Stock', 'Rating', 'Description', 'UPC', 'Price (excl. tax)',
				  'Price (incl. tax)']
	with open(nameFile, 'a') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writerow(allInfos)

def extract_and_transform_infos_from_html_page(allInfos, book):
	page_of_book = requests.get(book)
	soup_of_book = BeautifulSoup(page_of_book.content, 'html.parser')
	extract_and_transform_image_link(soup_of_book, allInfos)
	extract_and_transform_title_stock_available_and_rating(soup_of_book, allInfos)
	extract_and_transform_description(soup_of_book, allInfos)
	extract_and_transform_upc_and_price(soup_of_book, allInfos)

def extract_transform_load_all_infos_in_csv(book, nameFile):
	allInfos = {}
	extract_and_transform_infos_from_html_page(allInfos, book)
	load_infos_in_csv(allInfos, nameFile)
