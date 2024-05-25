#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import bs4
import requests
from bs4 import BeautifulSoup
import logging


class NewsScraper:
    def __init__(self):
        """
        'NewsScraper' class contains methods related to fetching URL and extracting data from news articles.
        """
        pass

    @staticmethod
    def fetch_and_parse_url(url: str) -> BeautifulSoup:
        """
        Fetch the content of a URL and parse it with BeautifulSoup.
        :param url: URL to parse.
        :return: BeautifulSoup object.
        """
        logging.info(f'Fetching URL: {url}')
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def get_unique_hrefs(self, url: str) -> list[str]:
        """
        Get a list of unique hrefs from the given URL.
        :param url: URL to parse.
        :return: List of unique hrefs.
        """
        logging.info(f'Get unique hrefs from {url}')
        soup = self.fetch_and_parse_url(url)
        href_list = self.extract_href_tags(soup)
        return list(set(href_list))

    @staticmethod
    def extract_href_tags(soup: BeautifulSoup) -> list[str]:
        """
        Extract all href attributes from anchor tags.
        :param soup: BeautifulSoup object.
        :return: List of href attributes.
        """
        logging.info(f'Extract href attributes with BeautifulSoup')
        href_tags = soup.find_all('a', href=True)
        return [tag['href'] for tag in href_tags]

    def extract_text_from_href_list(self, href_list: list[str]) -> list[str]:
        """
        Extract all text from the given href attributes.
        :param href_list: List of href attributes.
        :return: List of extracted texts.
        """
        logging.info('Extract news articles\' texts from a href list')
        text_list = []
        for href in href_list:
            url = 'https://www3.nhk.or.jp' + href

            inner_response = requests.get(url)
            inner_response.encoding = 'utf-8'
            inner_soup = BeautifulSoup(inner_response.text, 'html.parser')

            news_articles = self.find_all_news_articles(inner_soup)

            text_list += self.append_extracted_text(news_articles)

        if not text_list:
            logging.warning('No text extracted from the news articles')

        return text_list

    @staticmethod
    def find_all_news_articles(inner_soup) -> bs4.ResultSet:
        """
        Find all news articles from the section tag.
        :param inner_soup: BeautifulSoup object.
        :return: Set of the news articles found by BeautifulSoup.
        """
        logging.info('Find all news articles\' texts from section tags')
        news_articles: bs4.ResultSet = inner_soup.find_all('section', class_='content--detail-main')
        return news_articles

    @staticmethod
    def append_extracted_text(news_articles: bs4.ResultSet) -> list[str]:
        """
        Append the extracted text to a list.
        :param news_articles: Scraped news articles.
        :return: List of extracted texts from the scraped news articles.
        """
        logging.info('Append the extracted text from the scraped news articles to a list')
        news_article_list = []
        for news_article in news_articles:
            news_article_list.append(news_article.text)
        return news_article_list
