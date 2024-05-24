import requests
from bs4 import BeautifulSoup

url = 'https://www3.nhk.or.jp/news/'

response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all 'a' tags (anchor tags) which contain href attribute
href_tags = soup.find_all('a', href=True)

# Extract the href attribute value from each 'a' tag
href_list = []
for tag in href_tags:
    href = tag['href']
    print(href)
    href_list.append(href)

href_list = list(set(href_list))
for href in href_list:
    url = 'https://www3.nhk.or.jp' + href

    # Visit each URL
    inner_response = requests.get(url)
    inner_response.encoding = 'utf-8'
    inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

    # Example: Extract text from paragraph tags
    paragraphs = inner_soup.find_all('section', class_='content--detail-main')

    paragraph_list = []
    for paragraph in paragraphs:
        paragraph_list.append(paragraph.text)
        print(paragraph_list)

