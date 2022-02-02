import CategoryPage
from bs4 import BeautifulSoup
import requests
import csv

def create_csv_file(nameFile):
	fieldnames = ['Image_url', 'Title', 'Stock', 'Rating', 'Description', 'UPC', 'Price (excl. tax)',
				  'Price (incl. tax)']
	with open(nameFile, 'a') as file:
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		writer.writeheader()

alltheCategory = requests.get("https://books.toscrape.com/index.html")
soup = BeautifulSoup(alltheCategory.content, 'html.parser')
alltheCategory=soup.find('ul', class_ = 'nav nav-list')
alltheCategory=alltheCategory.ul.find_all('li')
for category in alltheCategory:
	categoryName = category.a.string.strip()
	nameFile = categoryName + ".csv"
	create_csv_file(nameFile)
	print(category.a.string.strip())
	category = "https://books.toscrape.com/" + category.a["href"]
	CategoryPage.extract_transform_load_all_books_infos_from_category(category, nameFile)
